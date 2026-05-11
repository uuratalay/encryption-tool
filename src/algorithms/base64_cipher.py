import base64
from src.algorithms.base import EncryptionAlgorithm


class Base64Cipher(EncryptionAlgorithm):
    """Base64 kodlama algoritması."""

    def encrypt(self, text):
        return base64.b64encode(text.encode()).decode()

    def decrypt(self, text):
        return base64.b64decode(text.encode()).decode()

    def get_name(self):
        return "Base64"
