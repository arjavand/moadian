import re
from datetime import datetime


class UniqueTaxID:
    def __init__(self, fiscalId):
        self.fiscalId = fiscalId

    def generate(self, invoice_date, serial_number):
        invoice_date_normalized = self.invoice_date_normalizer(invoice_date)
        invoice_date_hex16, date_utf8 = self.invoice_date_convert_to_hex16(invoice_date_normalized)
        serial_number_normalized = self.serial_number_normalizer(serial_number)
        serial_number_hex16 = self.serial_number_to_convert_hex16(serial_number_normalized)
        verhoeff_controller = self.verhoeff_calcsum(serial_number_normalized, date_utf8)
        return self.fiscalId + invoice_date_hex16 + serial_number_hex16 + verhoeff_controller

    def verhoeff_calcsum(self, serial_number_normalized, date_utf8):
        """For a given number returns a Verhoeff checksum digit"""

        verhoeff_table_d = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
            (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
            (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
            (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
            (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
            (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
            (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
            (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
            (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
        )
        verhoeff_table_p = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
            (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
            (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
            (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
            (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
            (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
            (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
        )
        verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)
        utf8 = self.alphabet_to_ord(self.fiscalId) + date_utf8 + serial_number_normalized
        c = 0
        for i, item in enumerate(reversed(str(utf8))):
            c = verhoeff_table_d[c][verhoeff_table_p[(i + 1) % 8][int(item)]]
        return str(verhoeff_table_inv[c])

    @staticmethod
    def alphabet_to_ord(item):
        """
        valid_alphabets = ["A", "D", "E", "F", "G", "H", "K", "M", "N", "O", "P", "R", "T", "W", "X", "Y", "Z"]
        invalid_alphabets = ["I", "J", "L", "Q", "V"]
        reserved_alphabets = ["B", "C", "S", "U"]
        """
        return "".join([str(ord(i)) if not i.isnumeric() else str(i) for i in item])

    @staticmethod
    def serial_number_normalizer(serial_number):
        serial_number = str(serial_number)
        if (diff := 12 - len(serial_number)) > 0:
            serial_number = "0" * diff + serial_number
        return serial_number

    @staticmethod
    def serial_number_to_convert_hex16(serial_number_normalized):
        return format(int(serial_number_normalized), "010X")

    @staticmethod
    def invoice_date_normalizer(invoice_date):
        if str(invoice_date).isnumeric():
            invoice_date = datetime.fromtimestamp(int(invoice_date) / 1000)
            invoice_date = invoice_date.strftime("%Y-%m-%d %H:%M:%S")
        invoice_date = invoice_date.replace("/", "-")
        regex = r"(\d{4}-\d{2}-\d{2}).*"
        return re.findall(regex, invoice_date)[0]

    @staticmethod
    def invoice_date_convert_to_hex16(date_normalized):
        date_utf8 = round(datetime.strptime(date_normalized, "%Y-%m-%d").timestamp() / 86400)
        if (diff := 6 - len(str(date_utf8))) >= 1:
            date_utf8 = diff * "0" + str(date_utf8)
        date_utf8_hex = hex(int(date_utf8))
        date_hex = "0" + "0" * (4 - len(date_utf8_hex[2:])) + date_utf8_hex[2:]
        invoice_date_hex16 = date_hex.upper()
        return invoice_date_hex16, date_utf8
