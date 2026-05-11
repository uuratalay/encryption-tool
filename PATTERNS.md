# Tasarım Örüntüleri Belgeleri

## Faz 1 — Creational Örüntüler

### Factory Method

**Nerede uygulandı:** `src/factory.py` → `AlgorithmFactory` sınıfı

**Neden uygulandı:**
Başlangıç kodunda algoritma seçimi `__init__`, `encrypt`, `decrypt` ve `export_to_file` metodlarının hepsinde if-else zincirleriyle yapılıyordu. Yeni bir algoritma eklemek için en az 4 farklı yeri değiştirmek gerekiyordu.

**Ne kazandık:**
- Her algoritma kendi sınıfında kapsüllendi
- Yeni algoritma eklemek = yeni sınıf yaz + `factory.register()` çağır
- Runtime'da algoritma değiştirmek mümkün hale geldi

---

## Faz 2 — Structural Örüntüler

### Adapter Pattern

**Nerede uygulandı:** `src/adapters.py` → `VigenereAdapter`, `AtbashAdapter`

**Neden uygulandı:**
Sisteme yeni algoritmalar eklemek istedik ama bunlar farklı API'lere sahip harici kütüphanelerden geliyordu. `VigenereCryptoLib` bizim `encrypt/decrypt` yerine `encode_text/decode_text` kullanıyor. `AtbashCryptoLib` ise sadece `transform` metodu sunuyor. Bu sınıfları doğrudan kullanamıyorduk.

**Alternatif: Facade mı?**
Facade karmaşık bir alt sistemi basitleştirir. Bizim sorunumuz basitleştirme değil, arayüz uyumsuzluğu — bu yüzden Adapter doğru seçim.

**Ne kazandık:**
- Harici kütüphanelerin koduna dokunmadan sisteme entegre ettik
- `EncryptionAlgorithm` arayüzü korundu — factory'ye direkt ekleyebildik
- İleride başka kütüphaneler de aynı yöntemle eklenebilir

**Önce → Sonra:**

Önce (harici kütüphane doğrudan kullanılsa):
```python
# Her yerde farklı API kontrolü gerekir
if isinstance(algo, VigenereCryptoLib):
    result = algo.encode_text(text)
elif isinstance(algo, AtbashCryptoLib):
    result = algo.transform(text)
else:
    result = algo.encrypt(text)
```

Sonra:
```python
# Adapter sayesinde tek bir arayüz
result = algo.encrypt(text)  # hangi algoritma olursa olsun
```

### Decorator Pattern

**Nerede uygulandı:** `src/decorators.py` → `LoggingDecorator`, `TimingDecorator`, `CompressionDecorator`

**Neden uygulandı:**
Algoritmalara loglama, süre ölçümü ve sıkıştırma gibi ek davranışlar eklemek istiyorduk. Bu davranışları her algoritma sınıfına ayrı ayrı yazmak kod tekrarı oluşturur ve algoritma sınıflarının sorumluluğunu artırır. Decorator ile bu davranışları bağımsız sınıflar olarak tanımlayıp istediğimiz algoritmaya runtime'da sardık.

**Ne kazandık:**
- Algoritma sınıfları temiz kaldı — sadece şifreleme/çözme işini yapıyorlar
- Ek davranışlar isteğe bağlı ve zincirleme eklenebilir
- Yeni bir davranış eklemek = yeni decorator sınıfı yazmak (mevcut koda dokunmaya gerek yok)

**Zincirleme kullanım örneği:**
```python
algo = CaesarCipher(3)
algo = LoggingDecorator(algo)      # loglama ekle
algo = TimingDecorator(algo)       # süre ölçümü ekle
# artık algo hem loglar, hem süre ölçer, hem şifreler
```

---

*Faz 3 tamamlandıkça güncellenecektir.*
