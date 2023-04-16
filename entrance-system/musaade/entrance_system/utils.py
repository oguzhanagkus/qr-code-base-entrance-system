import string
import random
import base64
import pyqrcode
import requests
from Crypto.Cipher import AES

from django.conf import settings


def ask_to_hes_api(hes_code):
    url = settings.HES_API_URL
    token = settings.HES_API_TOKEN
    headers = {"Content-Type": "application/json", "token": token}
    api_response = requests.get(url, headers=headers, json={"hes_code": hes_code}, verify=False)
    return api_response.json()


def generate_random_token(key_size: int) -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(key_size))


def api_token() -> str:
    return generate_random_token(64)


def secret_token() -> str:
    return generate_random_token(16)


class Cryptographer:
    def __init__(self, key: bytes = None, iv: bytes = None):
        self.key = key if key else settings.ENCRYPTION_KEY
        self.iv = iv if iv else settings.ENCRYPTION_IV
        self.block_size = 16
        self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)

    def encrypt(self, plain_text: str) -> bytes:
        plain_text = self.pad(plain_text.encode("utf-8"))
        cipher_text = self.aes.encrypt(plain_text)
        return base64.b64encode(cipher_text)

    def decrypt(self, cipher_text: bytes) -> str:
        cipher_text = base64.b64decode(cipher_text)
        plain_text = self.aes.decrypt(cipher_text)
        return self.unpad(plain_text).decode("utf-8")

    def pad(self, plain_text: bytes) -> bytes:
        padding_size = self.block_size - len(plain_text) % self.block_size
        padding = padding_size * chr(padding_size)
        return plain_text + bytes(padding, "utf-8")

    def unpad(self, plain_text: bytes) -> bytes:
        return plain_text[:-ord(plain_text[len(plain_text) - 1:])]


class HardwareInitializer:
    def __init__(self, ssid: str, password: str, token: str):
        self.ssid = ssid
        self.password = password
        self.token = token
        self.url = settings.HARDWARE_URL
        self.field_sizes = {"ssid": 32 + 1, "password": 64 + 1, "token": 96 + 1, "url": 64 + 1}

    def generate_qr_code_data(self) -> bytes:
        _ssid = self.ssid + "\x00" * (self.field_sizes["ssid"] - len(self.ssid))
        _password = self.password + "\x00" * (self.field_sizes["password"] - len(self.password))
        _token = self.token + "\x00" * (self.field_sizes["token"] - len(self.token))
        _url = self.url + "\x00" * (self.field_sizes["url"] - len(self.url))
        combined_data = _ssid + _password + _token + _url

        cryptographer = Cryptographer(settings.HARDWARE_KEY, settings.HARDWARE_IV)
        encrypted_data = cryptographer.encrypt(combined_data) + bytes("#", "utf-8")

        qr_code = pyqrcode.create(encrypted_data)
        qr_code_data = qr_code.png_as_base64_str(scale=25)
        qr_code_data = base64.b64decode(qr_code_data)

        return qr_code_data
