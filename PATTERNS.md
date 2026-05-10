# Tasarım Örüntüleri Belgeleri

## Faz 1 — Creational Örüntüler

### Factory Method

**Nerede uygulandı:** `src/factory.py` → `AlgorithmFactory` sınıfı

**Neden uygulandı:**
Başlangıç kodunda algoritma seçimi `__init__`, `encrypt`, `decrypt` ve `export_to_file` metodlarının hepsinde if-else zincirleriyle yapılıyordu. Yeni bir algoritma eklemek için en az 4 farklı yeri değiştirmek gerekiyordu. Bu Open/Closed prensibini ihlal ediyordu.

**Ne kazandık:**
- Her algoritma kendi sınıfında kapsüllendi (`CaesarCipher`, `Base64Cipher`, vb.)
- Yeni algoritma eklemek = yeni sınıf yaz + `factory.register()` çağır
- `Encryptor` sınıfı artık algoritma detaylarını bilmiyor, sadece `encrypt()`/`decrypt()` çağırıyor
- Runtime'da algoritma değiştirmek mümkün hale geldi (`set_algorithm()`)

**Önce → Sonra:**

Önce:
```python
# Encryptor.__init__ içinde
if algorithm == "caesar": ...
elif algorithm == "base64": ...
elif algorithm == "xor": ...
# ... 6 adet if-else

# Encryptor.encrypt içinde
if self.algorithm == "caesar": ...
elif self.algorithm == "base64": ...
# ... yine 6 adet if-else (aynı kontrol tekrarı)
```

Sonra:
```python
# Factory nesne üretimini hallediyor
algorithm = factory.create("caesar", {"shift": 3})
result = algorithm.encrypt(text)  # polimorfizm!
```

**UML Diyagramı:** `docs/diagrams/` klasöründe

---

*Faz 2 ve 3 tamamlandıkça güncellenecektir.*
