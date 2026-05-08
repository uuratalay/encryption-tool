"""Şifreleme Aracı birim testleri."""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms.caesar import CaesarCipher
from src.algorithms.base64_cipher import Base64Cipher
from src.algorithms.xor import XORCipher
from src.algorithms.reverse import ReverseCipher
from src.algorithms.hashing import MD5Hash, SHA256Hash
from src.adapters import VigenereAdapter, AtbashAdapter
from src.factory import AlgorithmFactory
from src.strategy import EncryptionStrategy
from src.observers import EncryptionEventManager, StatisticsCollector
from src.decorators import LoggingDecorator, TimingDecorator, CompressionDecorator


class TestCaesarCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        c = CaesarCipher(3)
        encrypted = c.encrypt("Merhaba")
        self.assertEqual(c.decrypt(encrypted), "Merhaba")

    def test_shift_value(self):
        c = CaesarCipher(1)
        self.assertEqual(c.encrypt("abc"), "bcd")

    def test_non_alpha_unchanged(self):
        c = CaesarCipher(3)
        self.assertEqual(c.encrypt("Hello, World!"), "Khoor, Zruog!")


class TestBase64Cipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        b = Base64Cipher()
        encrypted = b.encrypt("Test")
        self.assertEqual(b.decrypt(encrypted), "Test")


class TestXORCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        x = XORCipher("key")
        encrypted = x.encrypt("Hello")
        self.assertEqual(x.decrypt(encrypted), "Hello")

    def test_empty_key_raises(self):
        with self.assertRaises(ValueError):
            XORCipher("")


class TestReverseCipher(unittest.TestCase):
    def test_encrypt_decrypt(self):
        r = ReverseCipher()
        self.assertEqual(r.encrypt("Hello"), "olleH")
        self.assertEqual(r.decrypt("olleH"), "Hello")


class TestHashing(unittest.TestCase):
    def test_md5_consistency(self):
        m = MD5Hash()
        self.assertEqual(m.encrypt("test"), m.encrypt("test"))

    def test_sha256_consistency(self):
        s = SHA256Hash()
        self.assertEqual(s.encrypt("test"), s.encrypt("test"))

    def test_hash_not_reversible(self):
        m = MD5Hash()
        with self.assertRaises(NotImplementedError):
            m.decrypt("hash")


class TestAdapters(unittest.TestCase):
    def test_vigenere_encrypt_decrypt(self):
        v = VigenereAdapter("SECRET")
        encrypted = v.encrypt("Hello World")
        self.assertEqual(v.decrypt(encrypted), "Hello World")

    def test_atbash_encrypt_decrypt(self):
        a = AtbashAdapter()
        encrypted = a.encrypt("Hello")
        self.assertEqual(a.decrypt(encrypted), "Hello")


class TestFactory(unittest.TestCase):
    def test_create_caesar(self):
        f = AlgorithmFactory()
        algo = f.create("caesar", {"shift": 5})
        self.assertEqual(algo.get_name(), "Caesar (shift=5)")

    def test_create_unknown_raises(self):
        f = AlgorithmFactory()
        with self.assertRaises(ValueError):
            f.create("unknown")

    def test_get_available(self):
        f = AlgorithmFactory()
        available = f.get_available()
        self.assertIn("caesar", available)
        self.assertIn("vigenere", available)

    def test_register_new_algorithm(self):
        f = AlgorithmFactory()
        f.register("custom", lambda p: ReverseCipher())
        algo = f.create("custom")
        self.assertEqual(algo.encrypt("abc"), "cba")


class TestStrategy(unittest.TestCase):
    def test_set_and_execute(self):
        s = EncryptionStrategy()
        s.set_strategy(CaesarCipher(3))
        result = s.execute_encrypt("abc")
        self.assertEqual(result, "def")

    def test_no_strategy_raises(self):
        s = EncryptionStrategy()
        with self.assertRaises(RuntimeError):
            s.execute_encrypt("test")

    def test_change_strategy_runtime(self):
        s = EncryptionStrategy()
        s.set_strategy(CaesarCipher(3))
        r1 = s.execute_encrypt("abc")

        s.set_strategy(ReverseCipher())
        r2 = s.execute_encrypt("abc")

        self.assertNotEqual(r1, r2)
        self.assertEqual(r1, "def")
        self.assertEqual(r2, "cba")


class TestObserver(unittest.TestCase):
    def test_statistics_collector(self):
        em = EncryptionEventManager()
        stats = StatisticsCollector()
        em.subscribe(stats)

        em.notify_encrypt("Caesar", "hello", "khoor")
        em.notify_encrypt("Caesar", "world", "zruog")
        em.notify_decrypt("Base64", "VGVzdA==", "Test")
        em.notify_error("MD5", "Hash geri çözülemez")

        report = stats.get_report()
        self.assertEqual(report["toplam_sifreleme"], 2)
        self.assertEqual(report["toplam_cozme"], 1)
        self.assertEqual(report["toplam_hata"], 1)
        self.assertEqual(report["algoritma_kullanim"]["Caesar"], 2)

    def test_unsubscribe(self):
        em = EncryptionEventManager()
        stats = StatisticsCollector()
        em.subscribe(stats)
        em.unsubscribe(stats)

        em.notify_encrypt("Caesar", "hello", "khoor")
        self.assertEqual(stats.encrypt_count, 0)


class TestDecorators(unittest.TestCase):
    def test_logging_decorator(self):
        algo = CaesarCipher(3)
        logged = LoggingDecorator(algo)
        result = logged.encrypt("test")
        self.assertEqual(result, "whvw")
        self.assertEqual(len(logged.get_logs()), 1)

    def test_compression_decorator(self):
        algo = Base64Cipher()
        compressed = CompressionDecorator(algo)
        text = "tekrar tekrar tekrar tekrar tekrar"
        encrypted = compressed.encrypt(text)
        decrypted = compressed.decrypt(encrypted)
        self.assertEqual(decrypted, text)

    def test_decorator_chaining(self):
        algo = CaesarCipher(3)
        algo = LoggingDecorator(algo)
        algo = TimingDecorator(algo)
        result = algo.encrypt("test")
        self.assertEqual(result, "whvw")


if __name__ == "__main__":
    unittest.main()
