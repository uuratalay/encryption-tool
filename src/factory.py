from src.algorithms.caesar import CaesarCipher
from src.algorithms.base64_cipher import Base64Cipher
from src.algorithms.xor import XORCipher
from src.algorithms.reverse import ReverseCipher
from src.algorithms.hashing import MD5Hash, SHA256Hash


class AlgorithmFactory:
    """
    Factory Method ile algoritma nesnesi üretir.
    
    Yeni algoritma eklemek için:
    1. EncryptionAlgorithm'den türeyen yeni sınıf yaz
    2. Bu factory'ye register et
    
    Böylece mevcut kodu değiştirmeden yeni algoritma eklenebilir.
    """

    def __init__(self):
        self._creators = {}
        # varsayılan algoritmaları kaydet
        self._register_defaults()

    def _register_defaults(self):
        """Varsayılan algoritmaları kayıt eder."""
        self.register("caesar", lambda params: CaesarCipher(params.get("shift", 3)))
        self.register("base64", lambda params: Base64Cipher())
        self.register("xor", lambda params: XORCipher(params.get("key", "")))
        self.register("reverse", lambda params: ReverseCipher())
        self.register("hash-md5", lambda params: MD5Hash())
        self.register("hash-sha256", lambda params: SHA256Hash())

    def register(self, name, creator_fn):
        """Yeni bir algoritma kaydeder."""
        self._creators[name] = creator_fn

    def create(self, name, params=None):
        """
        Algoritma adına göre nesne üretir.
        
        Args:
            name: Algoritma adı (caesar, base64, xor, vb.)
            params: Algoritmaya özel parametreler (dict)
        
        Returns:
            EncryptionAlgorithm nesnesi
        
        Raises:
            ValueError: Bilinmeyen algoritma adı
        """
        if params is None:
            params = {}

        creator = self._creators.get(name)
        if not creator:
            available = ", ".join(self._creators.keys())
            raise ValueError(
                f"Bilinmeyen algoritma: '{name}'. "
                f"Desteklenen algoritmalar: {available}"
            )
        return creator(params)

    def get_available(self):
        """Kayıtlı algoritma isimlerini döndürür."""
        return list(self._creators.keys())
