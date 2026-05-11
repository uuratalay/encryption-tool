# Tasarım Örüntüleri Belgeleri

## Faz 1 — Creational Örüntüler

### Factory Method

**Nerede uygulandı:** `src/factory.py` → `AlgorithmFactory` sınıfı

**Neden uygulandı:**
Başlangıç kodunda algoritma seçimi if-else zincirleriyle yapılıyordu. Yeni algoritma eklemek 4 farklı yerde değişiklik gerektiriyordu.

**Ne kazandık:**
- Her algoritma kendi sınıfında kapsüllendi
- Yeni algoritma = yeni sınıf + `factory.register()`
- Runtime'da algoritma değiştirmek mümkün

---

## Faz 2 — Structural Örüntüler

### Adapter Pattern

**Nerede uygulandı:** `src/adapters.py` → `VigenereAdapter`, `AtbashAdapter`

**Neden uygulandı:**
Harici kütüphaneler (`VigenereCryptoLib`, `AtbashCryptoLib`) farklı API'lere sahip. Adapter, bu kütüphaneleri `EncryptionAlgorithm` arayüzüne uyduruyor.

**Neden Facade değil:**
Sorun alt sistem karmaşıklığı değil, arayüz uyumsuzluğu.

### Decorator Pattern

**Nerede uygulandı:** `src/decorators.py` → `LoggingDecorator`, `TimingDecorator`, `CompressionDecorator`

**Neden uygulandı:**
Loglama ve zamanlama gibi ek davranışlar algoritma sınıflarının sorumluluğu değil. Decorator ile bu davranışları bağımsız ve zincirleme eklenebilir hale getirdik.

---

## Faz 3 — Behavioral Örüntüler

### Strategy Pattern

**Nerede uygulandı:** `src/strategy.py` → `EncryptionStrategy` sınıfı

**Neden uygulandı:**
Factory algoritma nesnesini **üretir** ama nasıl kullanılacağını yönetmez. Strategy bir "context" sınıfı olarak algoritmayı kapsülleyip runtime'da değiştirmeyi sağlar. Encryptor artık hiçbir algoritmayı doğrudan bilmiyor — Strategy'ye delege ediyor.

**OCP gösterimi:**
Yeni bir algoritma eklemek için mevcut hiçbir dosyayı değiştirmek gerekmiyor:
1. `EncryptionAlgorithm`'den türeyen yeni sınıf yaz
2. `factory.register("yeni_algo", lambda p: YeniAlgo())` çağır
3. `enc.set_algorithm("yeni_algo")` ile kullan

Mevcut kodda tek satır değişiklik yok — sistem genişlemeye açık, değişikliğe kapalı.

### Observer Pattern

**Nerede uygulandı:** `src/observers.py` → `EncryptionEventManager`, `ConsoleLogger`, `StatisticsCollector`

**Neden uygulandı:**
Şifreleme olaylarına farklı bileşenlerin bağımsızca tepki vermesi gerekiyor. Decorator tek bir algoritmayı sarar (algoritma seviyesi), Observer ise tüm sistemi dinler (sistem seviyesi). Yeni bir dinleyici eklemek için `EncryptionObserver`'dan türetip `subscribe()` çağırmak yeterli.

**Ne kazandık:**
- Loglama, istatistik toplama gibi yan etkiler Encryptor'dan bağımsız
- Dinleyiciler birbirinden habersiz çalışıyor
- Yeni dinleyici eklemek mevcut kodu değiştirmiyor (OCP)
