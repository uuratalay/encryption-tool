from src.algorithms.base import EncryptionAlgorithm


class CaesarCipher(EncryptionAlgorithm):
    """Caesar şifreleme algoritması."""

    def __init__(self, shift=3):
        self.shift = shift

    def encrypt(self, text):
        result = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    result += chr((ord(char) - 65 + self.shift) % 26 + 65)
                else:
                    result += chr((ord(char) - 97 + self.shift) % 26 + 97)
            else:
                result += char
        return result

    def decrypt(self, text):
        result = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    result += chr((ord(char) - 65 - self.shift) % 26 + 65)
                else:
                    result += chr((ord(char) - 97 - self.shift) % 26 + 97)
            else:
                result += char
        return result

    def get_name(self):
        return f"Caesar (shift={self.shift})"
