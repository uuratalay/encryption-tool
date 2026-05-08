from src.factory import AlgorithmFactory


class Encryptor:
    """
    Şifreleme aracı.
    
    Artık algoritmalar Factory Method ile üretiliyor.
    Encryptor sadece kullanıcı ile algoritma arasında köprü kuruyor.
    """

    def __init__(self):
        self.factory = AlgorithmFactory()
        self.algorithm = None
        self.log = []

    def set_algorithm(self, name, params=None):
        """Aktif algoritmayı değiştirir."""
        self.algorithm = self.factory.create(name, params)

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
    print("=== Şifreleme Aracı ===")

    enc = Encryptor()
    algorithms = enc.get_available_algorithms()
    print(f"Algoritmalar: {', '.join(algorithms)}")

    algorithm = input("Algoritma seçin: ").strip().lower()

    params = {}
    if algorithm == "caesar":
        params["shift"] = int(input("Shift değeri girin: "))
    elif algorithm == "xor":
        params["key"] = input("XOR anahtarı girin: ")

    enc.set_algorithm(algorithm, params)

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
            enc.set_algorithm(new_algo, new_params)
            print(f"Algoritma değiştirildi: {new_algo}")
        elif choice == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    main()
