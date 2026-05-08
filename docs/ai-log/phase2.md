# Faz 2 — AI Kullanım Logu

## AI'a Ne Sordum

**Prompt 1:**
> "Adapter pattern burada uygun mu, yoksa Facade mı? Farkını açıkla."

**AI'ın Yanıtı (Özet):**
- **Adapter**: Mevcut bir sınıfın arayüzünü, beklenen başka bir arayüze dönüştürür. "Uyumsuz API'yi uyumlu hale getirmek" için kullanılır.
- **Facade**: Karmaşık bir alt sistemin önüne basit bir arayüz koyar. Birden fazla sınıfı tek noktadan yönetmek için kullanılır.
- Bizim durumda harici kütüphaneler (`VigenereCryptoLib`, `AtbashCryptoLib`) farklı metod adları kullanıyor — bu "arayüz uyumsuzluğu" sorunu, yani Adapter doğru seçim.
- Facade, mesela tüm şifreleme + dosya kaydetme + loglama işlemlerini tek bir basit API'den sunmak istesek uygun olurdu.

**Prompt 2:**
> "Loglama özelliğini eklemek için Decorator mı kullanmalıyım yoksa doğrudan Encryptor'a mı eklemeliyim?"

**AI'ın Yanıtı (Özet):**
- Decorator kullanmamı önerdi çünkü loglama, zamanlama gibi "ek davranışlar" algoritmanın asıl işi değil.
- Doğrudan eklersem her algoritma sınıfına log kodu yazmam gerekir — kod tekrarı olur.
- Decorator ile sarmalarsam istediğim algoritmaya istediğim davranışı runtime'da ekleyebilirim.
- Zincirleme decorator örneği verdi: `TimingDecorator(LoggingDecorator(CaesarCipher()))`.

**Prompt 3:**
> "CompressionDecorator şifreleme öncesi mi sonrası mı sıkıştırmalı?"

**AI'ın Yanıtı (Özet):**
- Şifrelemeden ÖNCE sıkıştırma yapılmalı dedi. Çünkü şifreli veri rastgele görünür ve sıkıştırılamaz.
- Doğru sıra: compress → encrypt. Çözme: decrypt → decompress.

## AI'ın Hatalı/Eksik Önerdiği Şey

AI başta Decorator pattern için `__getattr__` kullanarak "transparent proxy" yapısı önerdi. Yani decorator'ın sardığı nesnenin tüm metodlarını otomatik yönlendiren bir yapı. Bu ilk bakışta şık görünüyordu ama iki sorun vardı:

1. **Debugging zorlaşıyor**: `__getattr__` ile hangi metodun nereden çağrıldığını takip etmek zor.
2. **Açık değil**: Kodu okuyan biri decorator'ın ne yaptığını anlamak için `__getattr__` mekanizmasını bilmek zorunda.

Ben bunun yerine açık (explicit) bir `AlgorithmDecorator` base class yazdım — `encrypt`, `decrypt`, `get_name` metodlarını tek tek override ediyorum. Daha fazla kod ama daha okunabilir.

## Ne Uyguladım

### Adapter Pattern:
- `VigenereAdapter`: `VigenereCryptoLib`'in `encode_text/decode_text` API'sini `encrypt/decrypt`'e dönüştürüyor.
- `AtbashAdapter`: `AtbashCryptoLib`'in `transform` API'sini `encrypt/decrypt`'e dönüştürüyor.
- Her iki adapter da `EncryptionAlgorithm` arayüzünü implement ediyor, factory'ye sorunsuz eklendi.

### Decorator Pattern:
- `LoggingDecorator`: İşlem detaylarını loglar (girdi/çıktı uzunluk).
- `TimingDecorator`: İşlem süresini ölçer.
- `CompressionDecorator`: Şifrelemeden önce sıkıştırma yapar.
- Zincirleme kullanım: `TimingDecorator(LoggingDecorator(algo))` — iç içe sarmalama.

## Kazanımlar
- Harici kütüphaneler mevcut koda dokunmadan entegre edildi (Adapter).
- Loglama, zamanlama gibi davranışlar algoritma sınıflarını kirletmeden eklendi (Decorator).
- Kullanıcı runtime'da hangi ek davranışları istediğini seçebiliyor.
