import os
import base64
import binascii
from datetime import datetime
from typing import IO, BinaryIO
from Crypto.PublicKey import RSA
from _io import BufferedReader, TextIOWrapper


def key_validator(key: any, private: bool = True) -> any:
    _type = "PRIVATE" if private else "PUBLIC"
    if isinstance(key, (IO, BinaryIO, BufferedReader, TextIOWrapper)):
        key = key.read()
    elif type(key) == str:
        if os.path.isfile(key):
            with open(key, "rb") as file:
                key = file.read()
        elif not key.startswith("-----BEGIN"):
            key = f"-----BEGIN {_type} KEY-----\n{key.strip()}\n-----END {_type} KEY-----"
    try:
        RSA.import_key(base64.b64decode(key))
    except (binascii.Error, Exception) as e:
        raise ValueError(f"Invalid {_type.title()} key format. error({e})")
    return key


def timestamp_validator(timestamp: int) -> int:
    try:
        datetime.fromtimestamp(timestamp)
    except ValueError:
        return None
    return timestamp
