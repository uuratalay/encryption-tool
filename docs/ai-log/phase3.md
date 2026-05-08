# Faz 3 — AI Kullanım Logu (Pair Programming Oturumu)

## Oturum Özeti
AI ile yaklaşık 40 dakika pair programming yaptım. Strategy ve Observer pattern'lerinin nasıl uygulanacağını, OCP'nin nerede gösterileceğini ve CI pipeline kurulumunu tartıştık.

## Tartışma 1: Strategy vs mevcut yapı
**Ben:** "Faz 1'de Factory Method ile zaten algoritma seçiyoruz. Strategy ne ekstra getiriyor?"

**AI:** Factory Method nesneyi **üretir**, Strategy o nesneyi **kullanır**. İkisi farklı sorumluluklar. Factory "hangi nesne oluşturulacak" sorusunu çözer, Strategy "bu nesne nasıl kullanılacak ve runtime'da nasıl değiştirilecek" sorusunu çözer. Ayrı context sınıfı ile algoritmayı encapsulate etmek, Encryptor'ın algoritma detaylarından tamamen bağımsız kalmasını sağlıyor.

**Benim değerlendirmem:** Başta gereksiz gibi gelmişti ama kodu yazınca farkı gördüm. Encryptor artık hiçbir algoritma sınıfını doğrudan bilmiyor — sadece Strategy'ye delege ediyor.

## Tartışma 2: Observer nerede kullanılmalı?
**Ben:** "Loglama zaten Decorator ile yapılıyor. Observer'ı ne için kullanacağız?"

**AI:** Decorator tek bir algoritma nesnesini sarar ve o nesneye özgü ek davranış ekler. Observer ise **sistem genelinde** olayları dinler. Birden fazla bağımsız dinleyici aynı olaya tepki verebilir: biri loglar, biri istatistik toplar, biri e-posta atar. Bu dinleyiciler birbirinden habersiz.

**Benim değerlendirmem:** Mantıklı bir ayrım. Decorator algoritma seviyesinde, Observer sistem seviyesinde çalışıyor. İkisi birbirini tamamlıyor.

## Tartışma 3: OCP gösterimi
**Ben:** "Open/Closed prensibini nasıl gösterebilirim?"

**AI:** Yeni bir algoritma ekle ve göster ki hiçbir mevcut dosyayı değiştirmeden sisteme dahil oluyor. Factory'ye register et, Strategy ile kullan — mevcut kodda tek satır değişiklik yok.

**Benim değerlendirmem:** Bunu test kodunda da gösterdim — `test_register_new_algorithm` testi tam olarak bunu kanıtlıyor.

## Tartışma 4: CI pipeline
**AI:** GitHub Actions ile basit bir CI kurulumu önerdi — push ve PR'larda otomatik test çalıştırma. pytest kullanmamı önerdi.

**Benim değerlendirmem:** CI kurulumu düşündüğümden basitmiş. YAML dosyası 20 satır ve testleri otomatik çalıştırıyor.

## AI Beni Nerede Yanılttı?
AI başta Observer pattern için Python'un built-in `__set_name__` ve descriptor protocol'ünü kullanarak "reactive property" yapısı önerdi. Bu aşırı karmaşıktı ve ödev bağlamında anlaşılması zor olurdu. Basit bir event manager + subscriber yaklaşımı çok daha okunabilir ve anlaşılır. AI'ın "şık" çözümü her zaman "doğru" çözüm değil.

## AI Olmadan Bu Faz Ne Kadar Sürerdi?
Tahminen 2-3 kat daha uzun sürerdi. Strategy ve Observer'ın farkını anlamak, doğru yere uygulamak ve test yazmak en çok zorlandığım kısımlardı. AI özellikle "bu pattern neden burada gerekli" sorusuna somut cevaplar vererek kavramayı hızlandırdı. Ancak AI'ın her önerisini direkt uygulamak yerine basit ve okunabilir olanı seçmem gerektiğini de öğrendim.
