from abc import ABC, abstractmethod


class EncryptionObserver(ABC):
    """Observer arayüzü — şifreleme olaylarını dinler."""

    @abstractmethod
    def on_encrypt(self, algorithm_name, input_text, output_text):
        pass

    @abstractmethod
    def on_decrypt(self, algorithm_name, input_text, output_text):
        pass

    @abstractmethod
    def on_error(self, algorithm_name, error_message):
        pass


class EncryptionEventManager:
    """
    Observer Pattern: Şifreleme olaylarını yönetir.
    
    Subscriber'lar (observer'lar) kendilerini kayıt eder,
    bir olay gerçekleştiğinde tüm subscriber'lara bildirim gider.
    
    Yeni bir dinleyici eklemek için:
    1. EncryptionObserver'dan türet
    2. event_manager.subscribe(observer) çağır
    Mevcut koda dokunmaya gerek yok — OCP korunuyor.
    """

    def __init__(self):
        self._observers = []

    def subscribe(self, observer: EncryptionObserver):
        """Yeni bir observer ekler."""
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: EncryptionObserver):
        """Observer'ı çıkarır."""
        self._observers.remove(observer)

    def notify_encrypt(self, algorithm_name, input_text, output_text):
        """Şifreleme olayını tüm observer'lara bildirir."""
        for observer in self._observers:
            observer.on_encrypt(algorithm_name, input_text, output_text)

    def notify_decrypt(self, algorithm_name, input_text, output_text):
        """Çözme olayını tüm observer'lara bildirir."""
        for observer in self._observers:
            observer.on_decrypt(algorithm_name, input_text, output_text)

    def notify_error(self, algorithm_name, error_message):
        """Hata olayını tüm observer'lara bildirir."""
        for observer in self._observers:
            observer.on_error(algorithm_name, error_message)


class ConsoleLogger(EncryptionObserver):
    """Observer: İşlemleri konsola loglar."""

    def on_encrypt(self, algorithm_name, input_text, output_text):
        print(f"[LOG] {algorithm_name} | ENCRYPT | girdi: '{input_text[:30]}...' | çıktı: '{output_text[:30]}...'")

    def on_decrypt(self, algorithm_name, input_text, output_text):
        print(f"[LOG] {algorithm_name} | DECRYPT | girdi: '{input_text[:30]}...' | çıktı: '{str(output_text)[:30]}...'")

    def on_error(self, algorithm_name, error_message):
        print(f"[HATA] {algorithm_name} | {error_message}")


class StatisticsCollector(EncryptionObserver):
    """Observer: İşlem istatistiklerini toplar."""

    def __init__(self):
        self.encrypt_count = 0
        self.decrypt_count = 0
        self.error_count = 0
        self.algorithm_usage = {}

    def on_encrypt(self, algorithm_name, input_text, output_text):
        self.encrypt_count += 1
        self._track_usage(algorithm_name)

    def on_decrypt(self, algorithm_name, input_text, output_text):
        self.decrypt_count += 1
        self._track_usage(algorithm_name)

    def on_error(self, algorithm_name, error_message):
        self.error_count += 1

    def _track_usage(self, algorithm_name):
        if algorithm_name not in self.algorithm_usage:
            self.algorithm_usage[algorithm_name] = 0
        self.algorithm_usage[algorithm_name] += 1

    def get_report(self):
        """İstatistik raporu döndürür."""
        return {
            "toplam_sifreleme": self.encrypt_count,
            "toplam_cozme": self.decrypt_count,
            "toplam_hata": self.error_count,
            "algoritma_kullanim": self.algorithm_usage
        }
