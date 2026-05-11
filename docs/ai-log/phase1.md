# Faz 1 — AI Kullanım Logu

## AI'a Ne Sordum

**Prompt 1:**
> "Encryptor sınıfındaki if-else zincirlerini kırmak için hangi creational pattern kullanmalıyım? Factory Method mi, Abstract Factory mi?"

**AI'ın Yanıtı (Özet):**
- Factory Method önerdi çünkü tek bir ürün ailesi var (şifreleme algoritmaları). Abstract Factory birden fazla ilişkili ürün ailesi olduğunda kullanılır (mesela hem algoritma hem de key üreteci ailesi olsaydı).
- Bir `AlgorithmFactory` sınıfı oluşturmamı ve her algoritmayı ayrı sınıf olarak tanımlamamı söyledi.
- `register()` metodu ile yeni algoritmalar eklenebilir hale geleceğini belirtti.

**Prompt 2:**
> "Singleton pattern config yönetimi için gerekli mi bu projede?"

**AI'ın Yanıtı (Özet):**
- Şu an için gereksiz olduğunu söyledi. Singleton, global state yönetimi gerektiğinde mantıklı ama bu projede henüz paylaşılan bir konfigürasyon yok.
- "İhtiyaç yokken pattern eklemek over-engineering olur" dedi.

## Ne Uyguladım ve Neden

### Factory Method uyguladım:
- `EncryptionAlgorithm` abstract base class oluşturdum — tüm algoritmalar bunu implement ediyor.
- `AlgorithmFactory` sınıfında `register()` ve `create()` metodları ile algoritma üretimini merkezileştirdim.
- Her algoritma kendi sınıfında: `CaesarCipher`, `Base64Cipher`, `XORCipher`, `ReverseCipher`, `MD5Hash`, `SHA256Hash`.

### AI'dan farklı yaptığım şey:
- AI başta her algoritma için ayrı factory subclass önerdi (klasik Factory Method). Ben bunun yerine bir tane `AlgorithmFactory` ile `register/create` yaklaşımını tercih ettim çünkü Python'da ayrı factory sınıfları gereksiz karmaşıklık oluşturuyordu.
- Singleton'ı uygulamadım — AI de buna katıldı, gereksiz pattern eklemek kodu karıştırır.

### Singleton'ı neden uygulamadım:
- AI'ın dediği gibi, şu an paylaşılan bir global state yok.
- İleride gerekirse eklenebilir ama şu anki ihtiyaç için Factory Method yeterli.

## Kazanımlar
- `Encryptor` sınıfındaki 6 adet if-else bloğu tamamen kaldırıldı.
- Yeni algoritma eklemek için sadece yeni bir sınıf yazıp factory'ye register etmek yeterli.
- Runtime'da `set_algorithm()` ile algoritma değiştirilebiliyor (eski kodda yeni nesne oluşturmak gerekiyordu).
