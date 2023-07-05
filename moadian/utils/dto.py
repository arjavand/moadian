from typing import Union

key_types = {
    "taxid": str,  # 22 char / req / شماره منحصر به فرد مالیاتی
    "indatim": int,  # req / تاریخ و زمان صدور صورتحساب
    "Indati2m": int,  # special req / تاریخ و زمان ایجاد صورتحساب
    "inty": int,  # req / نوع صورتحساب
    "inno": str,  # opt / char 10 / سریال صورتحساب داخلی حافظه مالیاتی
    "irtaxid": str,  # special req / char 22 / شماره منحصر به فرد مالیاتی صورتحساب مرجع
    "inp": int,  # char 2 / req / الگوی صورتحساب
    "ins": int,  # char 1 / req / موضوع صورتحساب
    "tins": str,  # int as str / char 11-14 / req / شماره اقتصادی فروشنده
    "tinb": str,  # int as str / char 11-14 / special req / شماره اقتصادی خریدار
    "tob": int,  # char 1 / req as invoice pattern / نوع شخص خریدار
    "sbc": str,  # int as char / char 10 / opt / کد شعبه فروشنده
    "bid": str,  # int as char / char 10-12 / req as invoice pattern/ شناسه ملی/ شماره ملی/ شناسه مشارکت مدنی/ کد فراگیر اتباع غیرایرانی خریدار
    "bpc": str,  # int as char / char 10 / opt / کد پستی خریدار
    "bbc": str,  # int as char / char max 10 / opt / کد شعبه خریدار
    "bpn": str,  # char 9 / opt / شماره گذرنامه خریدار
    "ft": int,  # char 1 / req as invoice pattern / نوع پرواز
    "scln": str,  # int as char / char max 14 / req as invoice pattern / شماره پروانه گمرکی
    "scc": str,  # int as char / chr 5 / req as invoice pattern / کد گمرک محل اظهارفروشنده
    "crn": str,  # int as char / char max 12 / req as invoice pattern / شناسه یکتای ثبت قراردادفروشنده
    "cdcn": str,  # char max 14 / req as invoice pattern / شماره کوتاژ اظهارنامه گمرکی
    "cdcd": int,  # char 5 / req as invoice pattern / تاریخ کوتاژ اظهارنامه گمرکی
    "billid": str,  # int as char / char max 19 / req as invoice pattern / شماره اشتراک/ شناسه قبض بهره بردار
    "tprdis": int,  # char max 18 / req as invoice pattern / مجموع مبلغ قبل از کسر تخفیف
    "tdis": int,  # char max 18 / opt / مجموع تخفیفات
    "tadis": int,  # cha max 18 / req as invoice pattern / مجموع مبلغ پس از کسر تخفیف
    "tvam": int,  # char max 18 / req / مجموع مالیات بر ارزش افزوده
    "todam": int,  # char max 18 / req as invoice pattern / مجموع سایر مالیات، عوارض و وجوه قانونی
    "tbill": int,  # char max 18 / req / مجموع صورتحساب
    "tonw": float,  # int 16 - decimal 8 /  req as invoice pattern / مجموع وزن خالص
    "torv": int,  # char max 18 / req as invoice pattern / مجموع ارزش ریالی
    "tocv": float,  # int 14 - decimal 4 / req as invoice pattern / مجموع ارزش ارزی
    "setm": int,  # char 1 / req as invoice pattern / روش تسویه
    "cap": int,  # char max 18 / opt / مبلغ پرداختی نقدی
    "insp": int,  # char max 18 / opt / مبلغ نسیه
    "tvop": int,  # char max 18 / opt / مجموع سهم مالیات بر ارزش افزوده از پرداخت
    "Tax17": int,  # char max 18 / opt / مالیات موضوع ماده 17
    "sstid": str,  # int as char / req / char 13 / شناسه کاال/خدمت
    "sstt": str,  # opt / char max 400 / شرح کالا /خدمت
    "am": float,  # int max 18 - decimal max 8 / req / تعداد/مقدار
    "mu": str,  # int as char / max 8 char / opt / واحد اندازه گیری
    "nw": float,  # int max 15 - decimal max 8 / req as invoice pattern  / وزن خالص
    "fee": float,  # int max 18 - decimal max 8 / req as invoice pattern / مبلغ واحد
    "cfee": float,  # int max 14 - decimal max 4 / req as invoice pattern / میزان ارز
    "cut": str,  # char 3 / req as invoice pattern / نوع ارز
    "exr": int,  # char max 18 / req as invoice pattern / نرخ برابری ارز با ریال
    "ssrv": int,  # char max 18 / req as invoice pattern / ارزش ریالی کالا
    "sscv": float,  # int max 14 - decimal max 4 / req as invoice pattern / ارزش ارزی کالا
    "prdis": int,  # char max 18 / req as invoice pattern / مبلغ قبل از تخفیف
    "dis": int,  # char max 18 / req as invoice pattern / مبلغ تخفیف
    "adis": int,  # char max 18 / req as invoice pattern / مبلغ بعدازتخفیف
    "vra": float,  # int max 3 - decimal max 2 / req / نرخ مالیات برارزش افزوده
    "vam": int,  # char max 18 / req / مبلغ مالیات بر ارزش افزوده
    "odt": str,  # char max 255 / opt / موضوع سایر مالیات و عوارض
    "odr": float,  # int max 3 - decimal max 2 /  req as id of prod / نرخ سایر مالیات و عوارض
    "odam": int,  # char max 18 / req as invoice pattern / مبلغ سایر مالیات و عوارض
    "olt": str,  # char max 255 / opt / موضوع سایر وجوه قانونی
    "olr": float,  # int max 3 - decimal 2 / opt / نرخ سایر وجوه قانونی
    "olam": int,  # char max 18 / req as invoice pattern / مبلغ سایر وجوه قانونی
    "consfee": int,  # char max 18 / req as invoice pattern / اجرت ساخت
    "spro": int,  # char max 18 / req as invoice pattern / سودفروشنده
    "bros": int,  # char max 18 / req as invoice pattern / حق العمل
    "tcpbs": int,  # char max 18 / req as invoice pattern / جمع کل اجرت، حقالعمل و سود
    "cop": int,  # char max 18 / req as invoice pattern / سهم نقدی از پرداخت
    "vop": int,  # char max 18 / req as invoice pattern / سهم مالیات بر ارزش افزوده از پرداخت
    "bsrn": str,  # int as char / char max 12 / opt / شناسه یکتای ثبت قرارداد حق العمل کاری
    "tsstam": int,  # max char 18 / req / مبلغ کل کاال/خدمت
    "iinn": str,  # int as str / char 9 / req as invoice pattern / شماره سوییچ پرداخت
    "acn": str,  # int as str / char 14 / req as invoice pattern / شماره پذیرنده فروشگاهی
    "trmn": str,  # int as str / char 8 / req as invoice pattern /شماره پایانه
    "pmt": int,  # char max 2 / req as invoice pattern  / روش پرداخت
    "trn": str,  # int as str / char max 18 / req as invoice pattern / شماره پیگیری/ شماره مرجع
    "pcn": str,  # int as str / char 16 / req as invoice pattern / شماره کارت پرداخت کننده صورتحساب
    "pid": str,  # int as str / char max 12 / req as invoice pattern / شماره/ شناسه ملی/کد فراگیر پرداخت کننده صورتحساب
    "pdt": int,  # char 13 / req as invoice pattern / تاریخ و زمان پرداخت صورتحساب
    "pv": int,  # char max 18 / req as invoice pattern / مبلغ پرداختی
}


headers_keys = [
    "taxid",
    "indatim",
    "Indati2m",
    "inty",
    "inno",
    "irtaxid",
    "inp",
    "ins",
    "tins",
    "tob",
    "bid",
    "tinb",
    "sbc",
    "bpc",
    "bbc",
    "ft",
    "bpn",
    "scln",
    "scc",
    "crn",
    "billid",
    "tprdis",
    "tdis",
    "tadis",
    "tvam",
    "todam",
    "tbill",
    "setm",
    "cap",
    "insp",
    "tvop",
    "Tax17",
]

body_keys = [
    "sstid",
    "sstt",
    "am",
    "mu",
    "fee",
    "cfee",
    "cut",
    "exr",
    "prdis",
    "dis",
    "adis",
    "vra",
    "vam",
    "odt",
    "odr",
    "odam",
    "olt",
    "olr",
    "olam",
    "consfee",
    "spro",
    "bros",
    "tcpbs",
    "cop",
    "vop",
    "bsrn",
    "tsstam",
]

payment_keys = ["iinn", "acn", "trmn", "trn", "pcn", "pid", "pdt"]


def create_package(
    header: Union[dict, None] = None,
    body: Union[list, None] = None,
    payments: Union[list, None] = None,
    extension: Union[list, None] = None,
    **kwargs
) -> dict:
    if extension is None:
        extension = []
    if payments is None:
        payments = []
    if body is None:
        body = []
    if header is None:
        header = {}
    result = {
        "header": {},
        "body": [],
        "payments": [],
        "extension": extension,
    }
    _header = {}
    if header:
        for key in headers_keys:
            val = header.get(key, None)
            if val not in [None, ""]:
                _type = key_types[key]
                val = _type(val)
                _header[key] = val
        result["header"] = _header

    if body:
        for b in body:
            _body = {}
            for key in body_keys:
                val = b.get(key)
                if val not in [None, ""]:
                    _type = key_types[key]
                    val = _type(val)
                    _body[key] = val
            result["body"].append(_body)

    if payments:
        for payment in payments:
            _payments = {}
            for key in payment_keys:
                val = payment.get(key)
                if val not in [None, ""]:
                    _type = key_types[key]
                    val = _type(val)
                    _payments[key] = val
            result["payments"].append(_payments)

    if _header.get("inty") and int(_header.get("inty")) == 2:
        header.pop("setm", None)
    return result
