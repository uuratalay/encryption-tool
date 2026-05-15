# Faz 2 — Adapter + Decorator Patterns

Harici kütüphaneler Adapter ile entegre, ek davranışlar Decorator ile eklendi.

```mermaid
classDiagram
    class EncryptionAlgorithm {
        <<abstract>>
        +encrypt(text)* str
        +decrypt(text)* str
        +get_name()* str
    }

    class VigenereCryptoLib {
        +encode_text(text, key) str
        +decode_text(text, key) str
    }

    class AtbashCryptoLib {
        +transform(text) str
    }

    class VigenereAdapter {
        -lib: VigenereCryptoLib
        -key: str
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class AtbashAdapter {
        -lib: AtbashCryptoLib
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class BaseDecorator {
        #wrapped: EncryptionAlgorithm
        +encrypt(text) str
        +decrypt(text) str
        +get_name() str
    }

    class LoggingDecorator {
        +encrypt(text) str
        +decrypt(text) str
    }

    class TimingDecorator {
        +encrypt(text) str
        +decrypt(text) str
    }

    class CompressionDecorator {
        +encrypt(text) str
        +decrypt(text) str
    }

    EncryptionAlgorithm <|-- VigenereAdapter
    EncryptionAlgorithm <|-- AtbashAdapter
    EncryptionAlgorithm <|-- BaseDecorator
    BaseDecorator <|-- LoggingDecorator
    BaseDecorator <|-- TimingDecorator
    BaseDecorator <|-- CompressionDecorator
    VigenereAdapter --> VigenereCryptoLib : adapts
    AtbashAdapter --> AtbashCryptoLib : adapts
    BaseDecorator --> EncryptionAlgorithm : wraps
```

## Tasarım Kararları

- **Neden Facade değil Adapter?** Sorun alt sistem karmaşıklığı değil, arayüz uyumsuzluğu. Harici kütüphaneler encrypt/decrypt yerine encode_text/decode_text veya transform kullanıyor.
- **Decorator sırası önemli:** CompressionDecorator en içte olmalı — önce sıkıştır, sonra şifrele. Tersi yapılırsa şifreli veri rastgele olduğu için sıkıştırma işe yaramaz.
