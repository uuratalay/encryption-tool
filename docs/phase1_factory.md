# Faz 1 — Factory Method Pattern

Nesne yaratma sorumluluğu AlgorithmFactory'ye taşındı.

```mermaid
classDiagram
    class EncryptionAlgorithm {
        <<abstract>>
        +encrypt(text)* str
        +decrypt(text)* str
        +get_name()* str
    }

    class CaesarCipher {
        -shift: int
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class Base64Cipher {
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class XORCipher {
        -key: str
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class ReverseCipher {
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class MD5Hash {
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class SHA256Hash {
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class AlgorithmFactory {
        -_algorithms: dict
        +register(name, cls)
        +create(name, **kwargs) EncryptionAlgorithm
        +list_algorithms() list
    }

    class Encryptor {
        -factory: AlgorithmFactory
        -algorithm: EncryptionAlgorithm
        +encrypt(text) str
        +decrypt(text) str
    }

    EncryptionAlgorithm <|-- CaesarCipher
    EncryptionAlgorithm <|-- Base64Cipher
    EncryptionAlgorithm <|-- XORCipher
    EncryptionAlgorithm <|-- ReverseCipher
    EncryptionAlgorithm <|-- MD5Hash
    EncryptionAlgorithm <|-- SHA256Hash
    AlgorithmFactory --> EncryptionAlgorithm : creates
    Encryptor --> AlgorithmFactory : uses
    Encryptor --> EncryptionAlgorithm : delegates
```

## Çözülen Sorunlar

- ✅ if-else zincirleri kaldırıldı → Factory registry
- ✅ Nesne yaratma merkezi bir noktada → AlgorithmFactory
- ✅ Yeni algoritma = sadece yeni sınıf + register çağrısı
- ✅ Open/Closed Principle sağlandı
