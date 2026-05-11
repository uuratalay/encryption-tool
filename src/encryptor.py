from src.factory import AlgorithmFactory
from src.strategy import EncryptionStrategy
from src.observers import EncryptionEventManager, ConsoleLogger, StatisticsCollector
from src.decorators import LoggingDecorator, TimingDecorator, CompressionDecorator


class Encryptor:
    """
    Şifreleme Aracı — Tüm örüntülerin bir arada çalıştığı ana sınıf.
    
    Kullanılan örüntüler:
    - Factory Method: Algoritma nesnelerini üretir
    - Strategy: Runtime'da algoritma değiştirme
    - Observer: Olaylara tepki veren dinleyiciler (log, istatistik)
    - Decorator: Ek davranışlar (loglama, zamanlama, sıkıştırma)
    - Adapter: Harici kütüphaneleri ortak arayüze uyduruyor
    """

    def __init__(self):
        self.factory = AlgorithmFactory()
        self.strategy = EncryptionStrategy()
        self.event_manager = EncryptionEventManager()

    def set_algorithm(self, name, params=None, timing=False, compression=False):
        """
        Aktif algoritmayı değiştirir (Strategy pattern).
        İsteğe bağlı decorator'lar eklenebilir.
        """
        algo = self.factory.create(name, params)

        if compression:
            algo = CompressionDecorator(algo)
        if timing:
            algo = TimingDecorator(algo)

        self.strategy.set_strategy(algo)

    def encrypt(self, text):
        """Metni şifreler ve observer'lara bildirir."""
        algo = self.strategy.get_strategy()
        if not algo:
            raise RuntimeError("Önce bir algoritma seçin: set_algorithm()")

        try:
            result = self.strategy.execute_encrypt(text)
            self.event_manager.notify_encrypt(algo.get_name(), text, result)
            return result
        except Exception as e:
            self.event_manager.notify_error(algo.get_name(), str(e))
            raise

    def decrypt(self, text):
        """Şifreli metni çözer ve observer'lara bildirir."""
        algo = self.strategy.get_strategy()
        if not algo:
            raise RuntimeError("Önce bir algoritma seçin: set_algorithm()")

        try:
            result = self.strategy.execute_decrypt(text)
            self.event_manager.notify_decrypt(algo.get_name(), text, result)
            return result
        except NotImplementedError as e:
            self.event_manager.notify_error(algo.get_name(), str(e))
            print(f"HATA: {e}")
            return None

    def get_available_algorithms(self):
        """Kullanılabilir algoritmaları listeler."""
        return self.factory.get_available()


def main():
    print("=== Şifreleme Aracı v3 (Final) ===")

    enc = Encryptor()

    # Observer'ları ekle
    logger = ConsoleLogger()
    stats = StatisticsCollector()
    enc.event_manager.subscribe(logger)
    enc.event_manager.subscribe(stats)

    algorithms = enc.get_available_algorithms()
    print(f"Algoritmalar: {', '.join(algorithms)}")

    algorithm = input("Algoritma seçin: ").strip().lower()

    params = {}
    if algorithm == "caesar":
        params["shift"] = int(input("Shift değeri girin: "))
    elif algorithm == "xor":
        params["key"] = input("XOR anahtarı girin: ")
    elif algorithm == "vigenere":
        params["keyword"] = input("Vigenere anahtar kelime: ")

    use_timer = input("Süre ölçümü açık olsun mu? (e/h): ").strip().lower() == "e"
    enc.set_algorithm(algorithm, params, timing=use_timer)

    while True:
        print("\n1. Şifrele")
        print("2. Çöz")
        print("3. Algoritma Değiştir")
        print("4. İstatistikler")
        print("5. Çıkış")

        choice = input("Seçiminiz: ").strip()

        if choice == "1":
            text = input("Metin girin: ")
            result = enc.encrypt(text)
            print(f"Sonuç: {result}")
        elif choice == "2":
            text = input("Şifreli metin girin: ")
            result = enc.decrypt(text)
            if result:
                print(f"Sonuç: {result}")
        elif choice == "3":
            print(f"Algoritmalar: {', '.join(algorithms)}")
            new_algo = input("Yeni algoritma: ").strip().lower()
            new_params = {}
            if new_algo == "caesar":
                new_params["shift"] = int(input("Shift değeri: "))
            elif new_algo == "xor":
                new_params["key"] = input("XOR anahtarı: ")
            elif new_algo == "vigenere":
                new_params["keyword"] = input("Vigenere anahtar kelime: ")
            enc.set_algorithm(new_algo, new_params, timing=use_timer)
            print(f"Algoritma değiştirildi: {new_algo}")
        elif choice == "4":
            report = stats.get_report()
            print(f"\n--- İstatistikler ---")
            print(f"Toplam şifreleme: {report['toplam_sifreleme']}")
            print(f"Toplam çözme: {report['toplam_cozme']}")
            print(f"Toplam hata: {report['toplam_hata']}")
            print(f"Algoritma kullanımı: {report['algoritma_kullanim']}")
        elif choice == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    main()
