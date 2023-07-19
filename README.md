# Moadian
### Iranian Tax Organization API service(سرویس ارسال صورت حساب مالیاتی به سامانه مودیان) 

Developed by Arjavand Co (شرکت ارجاوند). 
[Arjavand.com](https://www.arjavand.com/)

#### installation:
```angular2html

>>> git clone https://github.com/arjavand/moadian

>>> python3 -m build 
    or 
    python3 setup.py sdist bdist_wheel 

>>> pip install dist/moadian-X.X.X.tar.gz

or 

>>> pip install moadian

```

#### Usage sample:
```angular2html
>>> from moadian.api import TaxApi

>>> org_api = TaxApi(
        private_key=PRIVATE_KEY,
        fiscalId=FISCAL_ID,
        economic_code=ECONOMIC_CODE,
    )

>>> org_api.get_server_information()

>>> org_api.get_token()

>>> packet = [{
            "serial_number" : int or None,
            "uid" : int or None,
            "header" : {
                "taxid": None,
                "indatim": None,
                "inty": 2,
                "irtaxid": None,
                "inp": 1,
                "ins": "1",
                "tins": "XXXXXXXXXXX",
                "tprdis": "",
                "tdis": "0",
                "tadis": "",
                "tvam": "",
                "todam": "",
                "tbill": "",
                "todam": "0",
            },
            "body" : [{
                "sstid": "XXXXXXXXXXXXXXXX",
                "sstt": "فروش بسته نرم افزاری سامانه ارتباطات ابری تلوبال",
                # "sstt": "Selling Telobal cloud communication system software package",
                "am": "XX",
                "fee": "XX",
                "prdis": "XX",
                "dis": "XX",
                "adis": "XX",
                "vra": "XX",
                "vam": "XX",
                "tsstam": "XXXXXX",
            }],
            "payment" : [{}]
        }]

>>> org_response = org_api.send_invoice(packet)
>>> org_response
    ({
            "signature": None,
            "signature_key_id": None,
            "timestamp": '1687686179',
            "result": [{
                "uid": 'c78812a5-fdc0-40ae-8672-eea0ddfadcbe',
                "referenceNumber": 'c78812a5-fdc0-40ae-8672-eea0ddfadcbe',
                "errorCode": None,
                "errorDetail": None
            }]
        },[{
            "serial_number": 'XXXX',
            "uid": 'c78812a5-fdc0-40ae-8672-eea0ddfadcbe',
            "unique_tax_id": 'XXXXXX00000000000000000',
            "indatim": '1687686179'
        }])


>>> org_api.get_inquiry_by_uid(ORG_RESPONSE_UID)

>>> org_api.cancel_invoice(UNIQUE_TAX_ID, NEW_SERIAL_NUMBER)
```

#### private or public key validator
```angular2html
>>> from moadian.utils.validators import key_validator

>>> key_validator(PRIVATE_KEY)

>>> key_validator(PUBLIC_KEY, private=False)
```

### Our Product (پروژه ها)
[Telobal](https://www.telobal.com/): Telephone Numbers and Cloud PBX (شماره تلفن و مرکز تماس ابری) [Telobal.com](https://www.telobal.com/)
