import re
import base64
from datetime import datetime
from Crypto.PublicKey import RSA


def key_validator(key: any, public: bool = False) -> any:
    new_private_key = re.findall(r"(-BEGIN[A-Za-z ]*KEY-)?\n?([^-]\n?)(-*END[A-Za-z ]*KEY-)?", key)
    try:
        if public:
            key = new_private_key[0][1].replace("\n", "")
            key = base64.b64decode(key)
        else:
            key = new_private_key[0][0] + "\n" + new_private_key[0][1].replace("\n", "") + "\n" + new_private_key[0][2]
        RSA.import_key(key)
        return key
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid {'Public' if public else 'Private'} key format. error({e})")


def timestamp_validator(timestamp: int) -> int:
    try:
        datetime.fromtimestamp(timestamp)
    except ValueError:
        return None
    return timestamp
