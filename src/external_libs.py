"""
Üçüncü parti şifreleme kütüphanesi simülasyonu.

Bu modül, farklı bir API'ye sahip harici bir kütüphaneyi temsil eder.
Gerçek projede bu cryptography, pycryptodome gibi bir kütüphane olabilir.
Bizim EncryptionAlgorithm arayüzümüzle uyumsuz.
"""


class VigenereCryptoLib:
    """
    Vigenere şifreleme - harici kütüphane gibi davranıyor.
    
    Dikkat: Bu sınıfın API'si bizim EncryptionAlgorithm'den farklı:
    - encrypt yerine encode_text kullanıyor
    - decrypt yerine decode_text kullanıyor
    - Constructor'da keyword alıyor (key değil)
    """

    def __init__(self, keyword):
        self.keyword = keyword.upper()

    def encode_text(self, plaintext):
        """Metni Vigenere ile şifreler."""
        result = []
        keyword_index = 0
        for char in plaintext:
            if char.isalpha():
                shift = ord(self.keyword[keyword_index % len(self.keyword)]) - 65
                if char.isupper():
                    result.append(chr((ord(char) - 65 + shift) % 26 + 65))
                else:
                    result.append(chr((ord(char) - 97 + shift) % 26 + 97))
                keyword_index += 1
            else:
                result.append(char)
        return "".join(result)

    def decode_text(self, ciphertext):
        """Şifreli metni Vigenere ile çözer."""
        result = []
        keyword_index = 0
        for char in ciphertext:
            if char.isalpha():
                shift = ord(self.keyword[keyword_index % len(self.keyword)]) - 65
                if char.isupper():
                    result.append(chr((ord(char) - 65 - shift) % 26 + 65))
                else:
                    result.append(chr((ord(char) - 97 - shift) % 26 + 97))
                keyword_index += 1
            else:
                result.append(char)
        return "".join(result)


class AtbashCryptoLib:
    """
    Atbash şifreleme - başka bir harici kütüphane.
    
    API yine farklı:
    - encrypt/decrypt yerine transform kullanıyor (çünkü Atbash kendi tersi)
    """

    def transform(self, text):
        """Atbash dönüşümü uygular (şifreleme = çözme)."""
        result = []
        for char in text:
            if char.isalpha():
                if char.isupper():
                    result.append(chr(90 - (ord(char) - 65)))
                else:
                    result.append(chr(122 - (ord(char) - 97)))
            else:
                result.append(char)
        return "".join(result)
