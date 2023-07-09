import os
import json
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding


class XOR:
    def do_xor(self, b1, b2):
        b1 = self.to_bytes(b1)
        b2 = self.to_bytes(b2)
        one_and_two = self.xor_blocks(b1, b2) if len(b1) < len(b2) else self.xor_blocks(b2, b1)
        length = len(one_and_two)
        while length > 0 and one_and_two[length - 1] == 0:
            length -= 1
        if length < len(one_and_two):
            return bytes(one_and_two[:length])
        return bytes(one_and_two)

    @staticmethod
    def to_bytes(data):
        if isinstance(data, dict):
            data = json.dumps(data).encode()
        elif isinstance(data, int):
            data = data.to_bytes((data.bit_length() + 7) // 8, "big")
        elif isinstance(data, str):
            data = data.encode()
        elif isinstance(data, bytearray):
            data = bytes(data)
        elif not isinstance(data, bytes):
            raise TypeError("Invalid data type. Supported types are hex, bytes, bytearray, and string.")
        return data

    @staticmethod
    def xor_blocks(smaller_array, bigger_array):
        one_and_two = bytearray(bigger_array)
        block_size = (len(bigger_array) + len(smaller_array) - 1) // len(smaller_array)
        for i in range(block_size):
            for j in range(len(smaller_array)):
                if (i * len(smaller_array)) + j >= len(bigger_array):
                    break
                one_and_two[(i * len(smaller_array)) + j] = (
                    smaller_array[j] ^ bigger_array[(i * len(smaller_array)) + j]
                )
        return bytes(one_and_two)

    @staticmethod
    def to_hex(data):
        return binascii.hexlify(data).decode()


class Encrypter:
    def __init__(self, tax_org_public_key, encryption_key_id):
        self.encryption_key_id = encryption_key_id
        self.tax_org_public_key = tax_org_public_key
        self.iv = os.urandom(16)

    @staticmethod
    def hex(bytes_array):
        return bytes_array.hex()

    @staticmethod
    def encrypt_symmetric_key(symmetric_key, public_key):
        public_key_bytes = base64.b64decode(public_key)
        public_key = serialization.load_der_public_key(public_key_bytes, backend=default_backend())
        encrypted_key = public_key.encrypt(
            symmetric_key.hex().encode("utf-8"),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        )
        encoded_encrypted_key = base64.b64encode(encrypted_key).decode("utf-8")
        return encoded_encrypted_key

    def encrypt(self, packets):
        aes_key = get_random_bytes(32)
        symmetric_key = self.encrypt_symmetric_key(aes_key, self.tax_org_public_key)
        for packet in packets:
            packet["iv"] = self.hex(self.iv)
            packet["encryptionKeyId"] = self.encryption_key_id
            packet["symmetricKey"] = symmetric_key
            packet["data"] = self.do_encryption(aes_key, packet["data"])

    def do_encryption(self, aes_key, data):
        if not isinstance(aes_key, bytes):
            aes_key = bytes.fromhex(aes_key)
        if not isinstance(self.iv, bytes):
            self.iv = bytes.fromhex(self.iv)
        if not isinstance(data, str):
            data = json.dumps(data)
        text_data = data.encode("utf-8")
        xor_text = XOR().do_xor(text_data, aes_key)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=self.iv)
        ciphertext, tag = cipher.encrypt_and_digest(xor_text)
        return base64.b64encode(ciphertext + tag).decode()

    def do_decryption(self, key, ciphertext):
        if not isinstance(self.iv, bytes):
            self.iv = bytes.fromhex(self.iv)
        ciphertext = base64.b64decode(ciphertext)
        tag = ciphertext[-16:]
        ciphertext = ciphertext[:-16]
        cipher = AES.new(key, AES.MODE_GCM, nonce=self.iv)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        xor_text = XOR().do_xor(plaintext, key).decode()
        return xor_text
