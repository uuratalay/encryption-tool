from abc import ABC, abstractmethod


class EncryptionAlgorithm(ABC):
    """Tüm şifreleme algoritmalarının temel sınıfı."""

    @abstractmethod
    def encrypt(self, text):
        """Metni şifreler."""
        pass

    @abstractmethod
    def decrypt(self, text):
        """Şifreyi çözer."""
        pass

    @abstractmethod
    def get_name(self):
        """Algoritma adını döndürür."""
        pass
