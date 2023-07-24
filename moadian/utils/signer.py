import base64
import os
from typing import IO, BinaryIO
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from _io import BufferedReader, TextIOWrapper


class Signer:
    def __init__(self, private_key: str):
        if isinstance(private_key, (IO, BinaryIO, BufferedReader, TextIOWrapper)):
            private_key = private_key.read()
        elif type(private_key) == str:
            if os.path.isfile(private_key):
                with open(private_key, "rb") as file:
                    private_key = file.read()
            elif not private_key.startswith("-----BEGIN"):
                private_key = f"-----BEGIN PRIVATE KEY-----\n{private_key.strip()}\n-----END PRIVATE KEY-----"
        self.private_key = RSA.import_key(private_key)

    def sign(self, data: str, public_key=None) -> str:
        try:
            hash_obj = SHA256.new(data.encode("utf-8"))
            signature = pkcs1_15.new(self.private_key).sign(hash_obj)
            signed = base64.b64encode(signature).decode("utf-8")
            if public_key:
                hash_obj = SHA256.new(data.encode("utf-8"))
                signature = base64.b64decode(signed)
                public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key.strip()}\n-----END PUBLIC KEY-----"
                rsa_key = RSA.import_key(public_key)
                verifier = pkcs1_15.new(rsa_key)
                verifier.verify(hash_obj, signature)
                print("sign verified successfully")
            return signed
        except (UnicodeEncodeError, ValueError, KeyError, Exception):
            raise NotImplementedError("invalid sign")

    @staticmethod
    def get_public_key_from_base64(key):
        try:
            byte_key = base64.b64decode(key)
            x509_public_key = RSA.import_key(byte_key)
            return x509_public_key
        except Exception:
            return None
