from src.factory import AlgorithmFactory
from src.decorators import LoggingDecorator, TimingDecorator, CompressionDecorator


class Encryptor:
    """
    Şifreleme aracı.
    
    Factory Method ile algoritma üretir.
    Decorator pattern ile ek davranışlar (loglama, zamanlama, sıkıştırma) ekler.
    """

    def __init__(self):
        self.factory = AlgorithmFactory()
        self.algorithm = None
        self.log = []

    def set_algorithm(self, name, params=None, logging=False, timing=False, compression=False):
        """
        Aktif algoritmayı değiştirir.
        
        Decorator'lar ile ek davranışlar eklenebilir:
        - logging: İşlemleri loglar
        - timing: Süre ölçer
        - compression: Sıkıştırma ekler
        """
        algo = self.factory.create(name, params)

        # decorator'ları zincirleme sar
        if compression:
            algo = CompressionDecorator(algo)
        if logging:
            algo = LoggingDecorator(algo)
        if timing:
            algo = TimingDecorator(algo)

        self.algorithm = algo

    def encrypt(self, text):
        """Metni aktif algoritma ile şifreler."""
        if not self.algorithm:
            raise RuntimeError("Önce bir algoritma seçin: set_algorithm()")
        result = self.algorithm.encrypt(text)
        self.log.append(f"[{self.algorithm.get_name()}] Şifrelendi: {text[:20]}...")
        return result

    def decrypt(self, text):
        """Şifreli metni aktif algoritma ile çözer."""
        if not self.algorithm:
            raise RuntimeError("Önce bir algoritma seçin: set_algorithm()")
        try:
            result = self.algorithm.decrypt(text)
            self.log.append(f"[{self.algorithm.get_name()}] Çözüldü: {text[:20]}...")
            return result
        except NotImplementedError as e:
            self.log.append(f"[{self.algorithm.get_name()}] Çözme başarısız: {e}")
            print(f"HATA: {e}")
            return None

    def show_log(self):
        """İşlem geçmişini gösterir."""
        if not self.log:
            print("Henüz işlem yapılmadı.")
        else:
            for entry in self.log:
                print(entry)

    def get_available_algorithms(self):
        """Kullanılabilir algoritmaları listeler."""
        return self.factory.get_available()


def main():
    print("=== Şifreleme Aracı v2 ===")

    enc = Encryptor()
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

    # Decorator seçenekleri
    use_log = input("Loglama açık olsun mu? (e/h): ").strip().lower() == "e"
    use_timer = input("Süre ölçümü açık olsun mu? (e/h): ").strip().lower() == "e"

    enc.set_algorithm(algorithm, params, logging=use_log, timing=use_timer)

    while True:
        print("\n1. Şifrele")
        print("2. Çöz")
        print("3. İşlem Geçmişi")
        print("4. Algoritma Değiştir")
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
            enc.show_log()
        elif choice == "4":
            print(f"Algoritmalar: {', '.join(algorithms)}")
            new_algo = input("Yeni algoritma: ").strip().lower()
            new_params = {}
            if new_algo == "caesar":
                new_params["shift"] = int(input("Shift değeri: "))
            elif new_algo == "xor":
                new_params["key"] = input("XOR anahtarı: ")
            elif new_algo == "vigenere":
                new_params["keyword"] = input("Vigenere anahtar kelime: ")
            enc.set_algorithm(new_algo, new_params, logging=use_log, timing=use_timer)
            print(f"Algoritma değiştirildi: {new_algo}")
        elif choice == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    main()
