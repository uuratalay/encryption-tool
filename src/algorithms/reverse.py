from src.algorithms.base import EncryptionAlgorithm


class ReverseCipher(EncryptionAlgorithm):
    """Ters çevirme algoritması."""

    def encrypt(self, text):
        return text[::-1]

    def decrypt(self, text):
        return text[::-1]

    def get_name(self):
        return "Reverse"
