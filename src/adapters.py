from src.algorithms.base import EncryptionAlgorithm
from src.external_libs import VigenereCryptoLib, AtbashCryptoLib


class VigenereAdapter(EncryptionAlgorithm):
    """
    Adapter: VigenereCryptoLib'i EncryptionAlgorithm arayüzüne uyduruyor.
    
    VigenereCryptoLib'in encode_text/decode_text metodları var,
    bizim sistemimiz encrypt/decrypt bekliyor. Bu adapter aradaki
    farkı kapatıyor.
    """

    def __init__(self, keyword):
        self._lib = VigenereCryptoLib(keyword)
        self._keyword = keyword

    def encrypt(self, text):
        return self._lib.encode_text(text)

    def decrypt(self, text):
        return self._lib.decode_text(text)

    def get_name(self):
        return f"Vigenere (key={self._keyword})"


class AtbashAdapter(EncryptionAlgorithm):
    """
    Adapter: AtbashCryptoLib'i EncryptionAlgorithm arayüzüne uyduruyor.
    
    AtbashCryptoLib'in sadece transform metodu var (şifreleme = çözme).
    Biz bunu encrypt ve decrypt olarak sunuyoruz.
    """

    def __init__(self):
        self._lib = AtbashCryptoLib()

    def encrypt(self, text):
        return self._lib.transform(text)

    def decrypt(self, text):
        return self._lib.transform(text)

    def get_name(self):
        return "Atbash"
