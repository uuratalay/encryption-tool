from src.algorithms.base import EncryptionAlgorithm


class EncryptionStrategy:
    """
    Strategy Pattern: Runtime'da algoritma değiştirmeyi sağlar.
    
    Bu sınıf bir "context" görevi görür — hangi algoritmanın
    kullanılacağını bilmez, sadece EncryptionAlgorithm arayüzüne
    güvenir ve delegasyon yapar.
    
    OCP (Open/Closed Principle) burada net görülür:
    - Yeni algoritma eklemek için bu sınıfa dokunmaya gerek yok
    - Sadece EncryptionAlgorithm'den türeyen yeni sınıf yazılır
    - set_strategy() ile runtime'da takılır
    """

    def __init__(self, algorithm: EncryptionAlgorithm = None):
        self._algorithm = algorithm

    def set_strategy(self, algorithm: EncryptionAlgorithm):
        """Runtime'da algoritmayı değiştirir."""
        self._algorithm = algorithm

    def get_strategy(self):
        """Aktif algoritmayı döndürür."""
        return self._algorithm

    def execute_encrypt(self, text):
        """Aktif strateji ile şifreler."""
        if not self._algorithm:
            raise RuntimeError("Strateji belirlenmedi. set_strategy() kullanın.")
        return self._algorithm.encrypt(text)

    def execute_decrypt(self, text):
        """Aktif strateji ile çözer."""
        if not self._algorithm:
            raise RuntimeError("Strateji belirlenmedi. set_strategy() kullanın.")
        return self._algorithm.decrypt(text)
