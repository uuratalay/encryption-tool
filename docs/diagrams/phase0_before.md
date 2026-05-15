# Faz 0 — Başlangıç Durumu (Refactoring Öncesi)

Tek bir Encryptor sınıfı tüm sorumluluğu taşıyor.

```mermaid
classDiagram
    class Encryptor {
        -algorithm: str
        -key: str
        -log: list
        +__init__(algorithm, key)
        +encrypt(text) str
        +decrypt(text) str
        +export_to_file(text, filename)
        +get_log() list
    }

    note for Encryptor "Sorunlar:\n1. God Class - tek sınıf her şeyi yapıyor\n2. if-else zincirleri 4 metotta tekrarlanıyor\n3. Yeni algoritma = 4 farklı yeri değiştir\n4. Runtime'da algoritma değiştirilemez\n5. Hash ve şifreleme karışmış"
```

## Sorun Özeti

- **7 farklı sorun** tespit edildi (bkz. PROBLEMS.md)
- En kritik sorun: nesne yaratma sorumluluğunun if-else zincirlerine dağılması
- Çözüm yolu: Design patterns ile sorumlulukları ayırmak
