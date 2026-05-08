from src.algorithms.base import EncryptionAlgorithm


class XORCipher(EncryptionAlgorithm):
    """XOR şifreleme algoritması."""

    def __init__(self, key):
        if not key:
            raise ValueError("XOR için key gerekli")
        self.key = key

    def encrypt(self, text):
        result = ""
        for i, char in enumerate(text):
            key_char = self.key[i % len(self.key)]
            result += chr(ord(char) ^ ord(key_char))
        return result

    def decrypt(self, text):
        # XOR kendi tersini alır
        return self.encrypt(text)

    def get_name(self):
        return "XOR"
