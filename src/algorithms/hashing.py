import hashlib
from src.algorithms.base import EncryptionAlgorithm


class MD5Hash(EncryptionAlgorithm):
    """MD5 hash algoritması."""

    def encrypt(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def decrypt(self, text):
        raise NotImplementedError("MD5 hash geri çözülemez")

    def get_name(self):
        return "MD5"


class SHA256Hash(EncryptionAlgorithm):
    """SHA-256 hash algoritması."""

    def encrypt(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def decrypt(self, text):
        raise NotImplementedError("SHA-256 hash geri çözülemez")

    def get_name(self):
        return "SHA-256"
