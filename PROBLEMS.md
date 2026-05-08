# Başlangıç Kodunun Sorun Analizi

## Benim Tespit Ettiğim Sorunlar

### 1. Her şey tek sınıfta (God Class)
`Encryptor` sınıfı hem şifreleme yapıyor, hem çözme yapıyor, hem log tutuyor, hem dosyaya yazıyor. Bir sınıf bu kadar farklı işi yapmamalı çünkü bir yeri değiştirmek istediğimde tüm sınıfı anlamam gerekiyor.

### 2. if-else zincirleri çok fazla
`encrypt()`, `decrypt()`, `export_to_file()` ve hatta `__init__` metodunun içinde bile aynı if-else kontrolü tekrarlanıyor. Yeni bir algoritma eklemek istesem en az 4-5 farklı yere kod yazmam lazım.

### 3. Algoritma ekleme sorunu (Kapalı değil)
Mesela "AES" eklemek istesem `__init__`, `encrypt`, `decrypt`, `export_to_file` hepsini değiştirmem gerekir. Yani mevcut kodu kırmadan yeni özellik eklemek imkansız.

### 4. Kod tekrarı (DRY ihlali)
`export_to_file` metoduna bakınca her algoritma için neredeyse aynı kodu tekrarlıyorum — sadece algoritma adı farklı. Log ekleme kısmı da her if bloğunun sonunda aynı şekilde tekrarlanıyor.

### 5. Runtime'da algoritma değiştirilemez
`__init__` içinde algoritma sabit kodlanmış. Program çalışırken "ben şimdi caesar yerine base64 kullanmak istiyorum" diyemiyorum, yeni bir nesne oluşturmam lazım.

### 6. Hash ve şifreleme karışmış
MD5 ve SHA-256 aslında hash fonksiyonu, şifreleme değil. Ama ben hepsini aynı sınıfa koydum. decrypt çağrılınca "geri çözülemez" diyor ama bu mantıksal olarak yanlış bir tasarım — hash ve encryption farklı kavramlar.

### 7. Test edilebilirlik sıfır
`main()` fonksiyonu `input()` ile çalışıyor, birim test yazmak çok zor. Sınıfın kendisi de o kadar büyük ki neyi test edeceğimi bilemiyorum.

---

## AI Analizi (Claude ile Karşılaştırma)

**AI'a sorduğum prompt:**
> "Bu kodda hangi tasarım sorunlarını görüyorsun? Hangi tasarım örüntüleri bu sorunları çözebilir? Her sorun için kısa bir açıklama yaz."

**AI'ın tespit ettiği sorunlar:**
1. **God Class / Single Responsibility ihlali** — Encryptor sınıfı çok fazla sorumluluk taşıyor. Her algoritma ayrı bir sınıf olmalı.
2. **Open/Closed Principle ihlali** — Yeni algoritma eklemek için mevcut kodu değiştirmek gerekiyor. Strategy veya Factory pattern ile çözülebilir.
3. **if-else zincirleri** — Polimorfizm ile ortadan kaldırılabilir. Her algoritma kendi sınıfında encrypt/decrypt metodunu implemente eder.
4. **Kod tekrarı** — Template Method veya base class ile ortak davranışlar çıkarılabilir.
5. **Hash ve şifreleme ayrımı yok** — Adapter veya ayrı interface'ler ile bu iki kavram birbirinden ayrılmalı.
6. **Loglama sıkı bağlı** — Observer pattern ile log mekanizması bağımsız hale getirilebilir.
7. **Nesne yaratma sorumluluğu dağınık** — Factory Method ile nesne oluşturma merkezi bir yere taşınabilir.

**Karşılaştırma:**
- Ben 7, AI da 7 sorun tespit etti. İlk 4 sorun (God Class, OCP ihlali, if-else, kod tekrarı) ikimizde de ortak.
- AI "Observer pattern ile loglama" önerdi — ben log sorununu fark etmiştim ama buna bir isim koyamamıştım.
- Ben "runtime'da algoritma değiştirilemez" demiştim, AI bunu "Strategy pattern" olarak isimlendirdi.
- Hash/encryption ayrımını ikimiz de gördük ama AI "Adapter" önerirken ben sadece "kavramsal olarak yanlış" demiştim.
- AI'ın "Template Method" önerisi benim aklıma gelmemişti — ortak davranışları base class'a çekme fikri mantıklı.

**Sonuç:** Sorunları görmek kolay ama çözüm için doğru örüntüyü bilmek gerekiyor. AI örüntü isimlerini benden daha net koydu, ben daha çok "bu yanlış hissettiriyor" seviyesinde kaldım.
