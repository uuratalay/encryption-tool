import time
import zlib
import base64
from src.algorithms.base import EncryptionAlgorithm


class AlgorithmDecorator(EncryptionAlgorithm):
    """
    Decorator base class.
    
    Bir EncryptionAlgorithm nesnesini sarmalayarak ek davranış ekler.
    Sarmalanan nesne de bir decorator olabilir — böylece davranışlar
    zincirleme eklenir.
    """

    def __init__(self, algorithm):
        self._wrapped = algorithm

    def encrypt(self, text):
        return self._wrapped.encrypt(text)

    def decrypt(self, text):
        return self._wrapped.decrypt(text)

    def get_name(self):
        return self._wrapped.get_name()


class LoggingDecorator(AlgorithmDecorator):
    """
    Decorator: Şifreleme/çözme işlemlerini loglar.
    
    Algoritmanın kendisini değiştirmeden loglama davranışı ekler.
    """

    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.logs = []

    def encrypt(self, text):
        result = self._wrapped.encrypt(text)
        log_entry = f"[LOG] [{self.get_name()}] encrypt çağrıldı | girdi uzunluk: {len(text)} | çıktı uzunluk: {len(result)}"
        self.logs.append(log_entry)
        print(log_entry)
        return result

    def decrypt(self, text):
        result = self._wrapped.decrypt(text)
        log_entry = f"[LOG] [{self.get_name()}] decrypt çağrıldı | girdi uzunluk: {len(text)} | çıktı uzunluk: {len(str(result))}"
        self.logs.append(log_entry)
        print(log_entry)
        return result

    def get_logs(self):
        return self.logs


class TimingDecorator(AlgorithmDecorator):
    """
    Decorator: Şifreleme/çözme süresini ölçer.
    
    Performans analizi için algoritmanın çalışma süresini kaydeder.
    """

    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.last_duration = 0

    def encrypt(self, text):
        start = time.time()
        result = self._wrapped.encrypt(text)
        self.last_duration = time.time() - start
        print(f"[TIMER] {self.get_name()} encrypt: {self.last_duration:.6f} saniye")
        return result

    def decrypt(self, text):
        start = time.time()
        result = self._wrapped.decrypt(text)
        self.last_duration = time.time() - start
        print(f"[TIMER] {self.get_name()} decrypt: {self.last_duration:.6f} saniye")
        return result


class CompressionDecorator(AlgorithmDecorator):
    """
    Decorator: Şifrelemeden önce metni sıkıştırır, çözmeden sonra açar.
    
    Büyük metinlerde şifreli çıktıyı küçültmek için kullanılır.
    Sıkıştırılmış veriyi base64 ile kodlar (binary-safe olması için).
    """

    def encrypt(self, text):
        # önce sıkıştır, sonra şifrele
        compressed = zlib.compress(text.encode())
        compressed_b64 = base64.b64encode(compressed).decode()
        return self._wrapped.encrypt(compressed_b64)

    def decrypt(self, text):
        # önce şifreyi çöz, sonra sıkıştırmayı aç
        decrypted = self._wrapped.decrypt(text)
        decompressed = zlib.decompress(base64.b64decode(decrypted))
        return decompressed.decode()

    def get_name(self):
        return f"{self._wrapped.get_name()} + Sıkıştırma"
