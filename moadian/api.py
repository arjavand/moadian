import re
import uuid
from typing import Union, BinaryIO

from moadian.utils.signer import Signer
from moadian.utils.decorators import token
from moadian.utils.request import TaxRequest
from moadian.utils.dto import create_package
from moadian.utils.encrypter import Encrypter
from moadian.utils.validators import key_validator, timestamp_validator
from moadian.utils.normalizer import JSONNormalizer
from moadian.utils.unique_tax_id import UniqueTaxID


class TaxApi(TaxRequest):
    __name__ = "moadian_api"

    TAX_API_URL = "https://tp.tax.gov.ir/req/api/self-tsp"
    TAX_API_VERSION = "01"

    def __init__(
        self,
        economic_code: int,
        fiscalId: str,
        private_key: Union[str, BinaryIO],
        public_key: Union[str, BinaryIO] = None,
        priority: str = "normal-enqueue",
        timestamp: Union[int, None] = None,
        get_token: bool = False,
        return_content=False,
    ) -> None:
        super().__init__()
        priority = priority if priority in ["normal-enqueue", "fast-enqueue"] else "normal-enqueue"
        self.token = None
        self.expires_in = None
        self.economic_code = economic_code
        self.fiscalId = fiscalId
        self.private_key = key_validator(private_key)
        self.public_key = (
            key_validator(public_key, private=False) if public_key else None
        )  # used for check sign verification
        self.sync_url = f"{self.TAX_API_URL}/sync"
        self.async_url = f"{self.TAX_API_URL}/async/{priority}"
        self.timestamp = timestamp_validator(timestamp) if timestamp else None
        self.return_content = return_content
        if get_token:
            self.get_token()

    @staticmethod
    def row_data_creator(packet: Union[list, dict], signature: str = None, time: int = 1, packets=False) -> dict:
        return {
            "time": time,
            "packet" if not packets else "packets": packet,
            "signature": signature,
            "signatureKeyId": None,
        }

    def packet_creator(self, packet_type: str, **kwargs: Union[dict, any]) -> dict:
        if uid := kwargs.get("uid", None):
            if isinstance(uid, bool):
                uid = str(uuid.uuid4())
        return {
            "uid": uid,
            "packetType": packet_type,
            "retry": str(kwargs.get("retry", "false")).lower(),
            "data": kwargs.get("data", None),
            "encryptionKeyId": kwargs.get("encryptionKeyId", ""),
            "symmetricKey": kwargs.get("symmetricKey", ""),
            "iv": kwargs.get("iv", ""),
            "fiscalId": self.fiscalId if kwargs.get("fiscalId", False) else "",
            "dataSignature": kwargs.get("dataSignature", ""),
        }

    def manager(
        self,
        url: str,
        packets: Union[list, dict, None] = None,
        headers: Union[dict, None] = None,
        token: bool = True,
        sign: bool = True,
    ) -> dict:
        signature = None
        if headers is None:
            headers = self.headers(token=token)
        if sign:
            normalized_packet = JSONNormalizer().normal_json(packets, headers)
            signature = Signer(self.private_key).sign(normalized_packet)
        data = self.row_data_creator(packet=packets, signature=signature, packets=isinstance(packets, list))
        self.request(url, data, headers)
        return self.response()

    @token
    def send_invoice(self, packets: list) -> tuple:
        """
        :param packets: [{
            "serial_number" : int or None,
            "uid" : int or None,
            "header" : {},
            "body" : [{}],
            "payment" : [{}]
        }]
        :return: ({
            "signature": None,
            "signature_key_id": None,
            "timestamp": '',
            "result": [{
                "uid": '',
                "referenceNumber": '',
                "errorCode": None,
                "errorDetail": None
            }]
        },[{
            "serial_number": '',
            "uid": '',
            "unique_tax_id": '',
            "indatim": ''
        }])
        """
        url = self.async_url
        headers = self.headers(token=self.token)
        full_packets = []
        packets_summary = []
        unique_tax_id = UniqueTaxID(self.fiscalId)
        for packet in packets:
            if "indatim" not in packet["header"] or packet["header"]["indatim"] is None:
                timestamp = headers.get("timestamp") if not self.timestamp else self.timestamp
                packet["header"]["indatim"] = timestamp
            else:
                timestamp = packet["header"]["indatim"]
            serial_number = packet.get("serial_number", 1)
            uid = packet.pop("uid", True)
            packet["header"]["tins"] = self.economic_code
            packet["header"]["taxid"] = unique_tax_id.generate(timestamp, serial_number)
            data = create_package(**packet)
            normalized_data = JSONNormalizer().normal_json(data)
            dataSignature = Signer(self.private_key).sign(normalized_data, public_key=self.public_key)
            packet_type = f"INVOICE.V{self.TAX_API_VERSION}"
            packet = self.packet_creator(
                packet_type=packet_type,
                **{
                    "uid": uid,
                    "data": data,
                    "dataSignature": dataSignature,
                    "fiscalId": True,
                },
            )
            full_packets.append(packet)
            packets_summary.append(
                {
                    "serial_number": serial_number,
                    "uid": packet["uid"],
                    "unique_tax_id": packet["data"]["header"]["taxid"],
                    "indatim": packet["data"]["header"]["indatim"],
                }
            )
        tax_public_keys = self.get_server_information().get("publicKeys")[0]
        public_key, public_key_id = tax_public_keys["key"], tax_public_keys["id"]
        encrypted_packets = Encrypter(public_key, public_key_id)
        encrypted_packets.encrypt(full_packets)
        return self.manager(url, packets=full_packets, headers=headers), packets_summary

    def get_server_information(self) -> dict:
        url = f"{self.sync_url}/GET_SERVER_INFORMATION"
        packet = self.packet_creator("GET_SERVER_INFORMATION")
        res = self.manager(url, packets=packet, token=False, sign=False)
        return res.get("result", {}).get("data", {})

    def get_token(self) -> dict:
        url = f"{self.sync_url}/GET_TOKEN"
        packet = self.packet_creator("GET_TOKEN", data={"username": f"{self.fiscalId}"})
        res = self.manager(url, packets=packet, token=False)
        res = res.get("result").get("data")
        self.token = res.get("token")
        self.expires_in = res.get("expires_in")
        return res

    @token
    def get_fiscal_information(self) -> dict:
        url = f"{self.sync_url}/GET_FISCAL_INFORMATION"
        packet = self.packet_creator("GET_FISCAL_INFORMATION", fiscalId=True)
        return self.manager(url, packets=packet)

    @token
    def get_economic_code_information(self, economic_code: Union[str, int, None] = None) -> dict:
        economic_code = self.economic_code if economic_code is None else economic_code
        url = f"{self.sync_url}/GET_ECONOMIC_CODE_INFORMATION"
        packet = self.packet_creator("GET_ECONOMIC_CODE_INFORMATION", data={"economicCode": f"{economic_code}"})
        return self.manager(url, packets=packet)

    @token
    def get_inquiry_by_uid(self, uids: Union[list, str]) -> dict:
        url = f"{self.sync_url}/INQUIRY_BY_UID"
        data = (
            [{"uid": i, "fiscalId": self.fiscalId} for i in uids]
            if isinstance(uids, list)
            else [{"uid": uids, "fiscalId": self.fiscalId}]
        )
        packet = self.packet_creator("INQUIRY_BY_UID", data=data)
        return self.manager(url, packets=packet)

    @token
    def get_inquiry_by_reference_number(self, reference_numbers: Union[list, str]) -> dict:
        if not isinstance(reference_numbers, (str, list)):
            raise TypeError("Type of reference_numbers must be str or list")
        url = f"{self.sync_url}/INQUIRY_BY_REFERENCE_NUMBER"
        data = {"referenceNumber": reference_numbers if isinstance(reference_numbers, list) else [reference_numbers]}
        packet = self.packet_creator("INQUIRY_BY_REFERENCE_NUMBER", data=data, fiscalId=True)
        return self.manager(url, packets=packet)

    @token
    def get_inquiry_by_time(self, time: str) -> dict:  # jalali format YYYYMMDD
        if not isinstance(time, (str, int)):
            raise ValueError("Type of time must be string or integer")
        # TODO: complete regex for jalali format
        if not re.match(r"\d{8}", str(time)):
            raise ValueError("Time must be like YYYYMMDD and jalali format 14010321")
        url = f"{self.sync_url}/INQUIRY_BY_TIME"
        packet = self.packet_creator("INQUIRY_BY_TIME", data={"time": int(time)})
        return self.manager(url, packets=packet)

    @token
    def get_inquiry_by_time_range(
        self, start_date: Union[str, int], end_date: Union[str, int]
    ) -> dict:  # jalali format YYYYMMDD
        # TODO: complete regex for jalali format
        url = f"{self.sync_url}/INQUIRY_BY_TIME_RANGE"
        if not any(
            [
                isinstance(start_date, (str, int)),
                isinstance(end_date, (str, int)),
            ]
        ):
            raise ValueError("Type of start_date or end_date must be string or integer")
        if not any(
            [
                re.match(r"\d{8}", str(start_date)),
                re.match(r"\d{8}", str(end_date)),
            ]
        ):
            raise ValueError("start_date and end_date must be like YYYYMMDD and jalali format 14010321")
        data = {"startDate": int(start_date), "endDate": int(end_date)}
        packet = self.packet_creator("INQUIRY_BY_TIME_RANGE", data=data)
        return self.manager(url, packets=packet)

    @token
    def get_service_stuff_list(self, filters=None, order_by=None, page: int = 1, size: int = 10) -> dict:
        if order_by is None:
            order_by = []
        if filters is None:
            filters = []
        url = f"{self.sync_url}/GET_SERVICE_STUFF_LIST"
        data = {"page": page, "size": size}
        if filters:
            data["filters"] = filters
        if order_by:
            data["orderBy"] = order_by
        packet = self.packet_creator("GET_SERVICE_STUFF_LIST", data=data)
        return self.manager(url, packets=packet)

    @token
    def cancel_invoice(self, invoice_unique_id: str, serial_number: int) -> tuple:
        packets = [
            {
                "serial_number": serial_number,
                "header": {
                    "taxid": None,
                    "indatim": None,
                    "irtaxid": invoice_unique_id,
                    "ins": 3,
                    "tins": self.economic_code,
                },
            }
        ]
        return self.send_invoice(packets)
