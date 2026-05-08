import base64
import hashlib


class Encryptor:
    """Şifreleme aracı - tüm algoritmalar tek sınıfta."""

    def __init__(self, algorithm, key=None):
        self.algorithm = algorithm
        self.key = key
        self.log = []

        # algoritma kontrolü
        if algorithm == "caesar":
            if key is None:
                self.key = 3
            elif not isinstance(key, int):
                raise ValueError("Caesar için key tam sayı olmalı")
        elif algorithm == "base64":
            pass  # key gerekmez
        elif algorithm == "xor":
            if key is None:
                raise ValueError("XOR için key gerekli")
        elif algorithm == "reverse":
            pass
        elif algorithm == "hash-md5":
            pass
        elif algorithm == "hash-sha256":
            pass
        else:
            raise ValueError(f"Desteklenmeyen algoritma: {algorithm}")

    def encrypt(self, text):
        """Metni şifreler."""
        if self.algorithm == "caesar":
            result = ""
            for char in text:
                if char.isalpha():
                    shift = self.key
                    if char.isupper():
                        result += chr((ord(char) - 65 + shift) % 26 + 65)
                    else:
                        result += chr((ord(char) - 97 + shift) % 26 + 97)
                else:
                    result += char
            self.log.append(f"[caesar] Şifrelendi: {text[:20]}...")
            return result

        elif self.algorithm == "base64":
            result = base64.b64encode(text.encode()).decode()
            self.log.append(f"[base64] Şifrelendi: {text[:20]}...")
            return result

        elif self.algorithm == "xor":
            result = ""
            for i, char in enumerate(text):
                key_char = self.key[i % len(self.key)]
                result += chr(ord(char) ^ ord(key_char))
            self.log.append(f"[xor] Şifrelendi: {text[:20]}...")
            return result

        elif self.algorithm == "reverse":
            result = text[::-1]
            self.log.append(f"[reverse] Şifrelendi: {text[:20]}...")
            return result

        elif self.algorithm == "hash-md5":
            result = hashlib.md5(text.encode()).hexdigest()
            self.log.append(f"[md5] Hash oluşturuldu: {text[:20]}...")
            return result

        elif self.algorithm == "hash-sha256":
            result = hashlib.sha256(text.encode()).hexdigest()
            self.log.append(f"[sha256] Hash oluşturuldu: {text[:20]}...")
            return result

    def decrypt(self, text):
        """Şifreyi çözer."""
        if self.algorithm == "caesar":
            result = ""
            for char in text:
                if char.isalpha():
                    shift = self.key
                    if char.isupper():
                        result += chr((ord(char) - 65 - shift) % 26 + 65)
                    else:
                        result += chr((ord(char) - 97 - shift) % 26 + 97)
                else:
                    result += char
            self.log.append(f"[caesar] Çözüldü: {text[:20]}...")
            return result

        elif self.algorithm == "base64":
            result = base64.b64decode(text.encode()).decode()
            self.log.append(f"[base64] Çözüldü: {text[:20]}...")
            return result

        elif self.algorithm == "xor":
            # xor kendi tersini alır
            result = ""
            for i, char in enumerate(text):
                key_char = self.key[i % len(self.key)]
                result += chr(ord(char) ^ ord(key_char))
            self.log.append(f"[xor] Çözüldü: {text[:20]}...")
            return result

        elif self.algorithm == "reverse":
            result = text[::-1]
            self.log.append(f"[reverse] Çözüldü: {text[:20]}...")
            return result

        elif self.algorithm == "hash-md5" or self.algorithm == "hash-sha256":
            print("HATA: Hash fonksiyonları geri çözülemez!")
            self.log.append(f"[{self.algorithm}] Çözme denemesi başarısız")
            return None

    def show_log(self):
        """İşlem geçmişini gösterir."""
        if len(self.log) == 0:
            print("Henüz işlem yapılmadı.")
        else:
            for entry in self.log:
                print(entry)

    def export_to_file(self, text, filename):
        """Sonucu dosyaya yazar."""
        if self.algorithm == "caesar":
            with open(filename, "w") as f:
                f.write(f"Algoritma: Caesar (shift={self.key})\n")
                f.write(f"Sonuç: {text}\n")
        elif self.algorithm == "base64":
            with open(filename, "w") as f:
                f.write(f"Algoritma: Base64\n")
                f.write(f"Sonuç: {text}\n")
        elif self.algorithm == "xor":
            with open(filename, "w") as f:
                f.write(f"Algoritma: XOR\n")
                f.write(f"Sonuç: {text}\n")
        elif self.algorithm == "reverse":
            with open(filename, "w") as f:
                f.write(f"Algoritma: Reverse\n")
                f.write(f"Sonuç: {text}\n")
        elif self.algorithm == "hash-md5":
            with open(filename, "w") as f:
                f.write(f"Algoritma: MD5\n")
                f.write(f"Sonuç: {text}\n")
        elif self.algorithm == "hash-sha256":
            with open(filename, "w") as f:
                f.write(f"Algoritma: SHA-256\n")
                f.write(f"Sonuç: {text}\n")
        self.log.append(f"Dosyaya yazıldı: {filename}")


def main():
    print("=== Şifreleme Aracı ===")
    print("Algoritmalar: caesar, base64, xor, reverse, hash-md5, hash-sha256")

    algorithm = input("Algoritma seçin: ").strip().lower()

    key = None
    if algorithm == "caesar":
        key = int(input("Shift değeri girin: "))
    elif algorithm == "xor":
        key = input("XOR anahtarı girin: ")

    enc = Encryptor(algorithm, key)

    while True:
        print("\n1. Şifrele")
        print("2. Çöz")
        print("3. İşlem Geçmişi")
        print("4. Dosyaya Kaydet")
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
            text = input("Kaydedilecek metin: ")
            filename = input("Dosya adı: ")
            enc.export_to_file(text, filename)
            print(f"{filename} dosyasına kaydedildi.")
        elif choice == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    main()
