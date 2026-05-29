# Ozellikler

Bu belge manga gorsel ceviricisinin temel ozelliklerini ve gorsel duzenleyicisini tanitir.

---

## Temel Ozellikler

### Metin Isleme

- **Akilli Metin Algilama**: Mangadaki metin bolgelerini otomatik tanir
- **Cok Dilli OCR**: Japonca, Cince, Ingilizce ve daha fazlasini destekler
- **5 Ceviri Motoru**: OpenAI, Gemini (standart + yuksek kalite), Sakura
- **Yuksek Kaliteli Ceviri**: Cok modlu AI modelleri kullanir (GPT-4o, Gemini); gorsel baglaminla birlikte ceviri yapar, dogruluk daha yuksek
- **Otomatik Terim Cikarimi**: AI ozgun isimleri (kisi adlari, yer adlari, organizasyon adlari vb.) otomatik tanir ve biriktirir; uzun ceviri tutarliligini korur
- **Gorsel Onarim**: Orijinal metni otomatik siler ve arka plani akillica doldurur
- **Akilli Metin Yerlesimi**: Ceviriyi otomatik dizer; birden fazla yazi tipi ve stili destekler
- **AI Satir Sonu**: Okunabilirligi arttirir; OpenAI ve Gemini ceviricileri icin akilli satir sonu destekler
- **Toplu Isleme**: Bir klasordeki tum gorselleri tek seferde isler
- **PSD Disa Aktarimi**: Duzenlenebilir PSD dosyalari disa aktarir (katmanlar: orijinal, onarilmis, metin)

---

## Gorsel Duzenleyici

Ceviri sonuclarini hassas olarak ayarlamak icin guclu grafik duzenleme araclari saglar:

### Alan Duzenleme

- **Tasima**: Metin bolgesini istenen konuma surukle
- **Dondurme**: Dondurme tutamaciyla 0-360 derece hassas dondurme
- **Sekil Degistirme**: Kose duzenleme, kenar ayarlamasi, serbest sekil degistirme
- **Sekil Duzenle**: Metin kutusunu sectikten sonra arac cubugundaki "Sekil Duzenle" dugmesine tiklayin; bos bolgede kose gen surerek yeni mavi kutu ekleyin

> OCR Tanima En Iyi Uygulamasi: Duzenleyicide metin kutularini ayarlayin; **bir mavi kutuda yalnizca bir satir** olmak uzere duzenlenmesini saglayin. Aksi takdirde 48px ve 32px modelleri metni dogru taniyamayabilir.

### Metin Duzenleme

- **Manuel Ceviri**: Ceviri icerigi dogrudan duzenleyin
- **Stil Ayarlamasi**: Yazi tipi, boyut, renk, hizalama
- **Yon Kontrolu**: Yatay/dikey yazi yonu

### Maske Duzenleme

- **Firca Araci**: Metin silme bolgesi elle cizin
- **Silgi**: Maske hatalarini duzeltir
- **Maske Optimizasyonu**: Silme etkisini otomatik optimize eder

### Gelismis Ozellikler

- **Geri Al/Yeniden Yap**: Tam islem gecmisi yonetimi
- **Toplu Islem**: Coklu secim, ozellikleri toplu degistirme
- **Gercek Zamanli Onizleme**: Ceviri etkisini aninda goruntuleyin

---

## Kullanici Arayuzu

- **Modern Tasarim**: PyQt6 tabanli akici arayuz
- **Surukle Birak Destegi**: Gorselleri dogrudan pencereye surukleyin
- **Gercek Zamanli Gunluk**: Ceviri ilerlemesini ve hata bilgilerini goruntuleyin
- **Yapilandirma Yonetimi**: Ozel yapilandirmalari kaydedin ve yukleyin

---

## Cevirici Destegi

### Cevrimici Ceviriciler (API Key Gerektirir)

| Cevirici | Aciklama |
|----------|----------|
| **OpenAI** | OpenAI ChatGPT cevirisi |
| **Gemini** | Google Gemini cevirisi |
| **Sakura** | Japonca icin ozel optimize edilmis ceviri modeli |

### Yuksek Kaliteli Ceviriciler (API Key Gerektirir, Onerilen)

| Cevirici | Avantaj |
|----------|---------|
| **Yuksek Kaliteli OpenAI** | GPT-4o gibi cok modlu modeller kullanir; gorsel baglaminla ceviri yapar |
| **Yuksek Kaliteli Gemini** | Gemini cok modlu modeli kullanir; gorsel baglaminla ceviri yapar |

**Yuksek Kaliteli Ceviricilerin Avantajlari**:
- Cok Modlu Anlama: AI gorsel icerigi "gorebilir" ve baglamı anlar
- Daha Dogru: Gorsel bilgiyle birlestirilmis, sahneye daha uygun ceviri
- Toplu Isleme: Bir seferde birden fazla gorsel gonderilir; AI genel konuyu anlar
- Ozel Ipucu: Ozel ceviri tarzini ve terim listesini destekler

### Diger Secenekler

| Secenek | Aciklama |
|---------|----------|
| **Orijinal** | Cevirmez; orijinal metni korur |
| **Hic** | Yalnizca metin algilar ve siler; ceviri yapilmaz |

---

## OCR Modelleri

| Model | Aciklama |
|-------|----------|
| **48px** | Varsayilan model, kullanim icin onerilen |
| **48px_ctc** | CTC modeli, daha yuksek tanima dogrulugu |
| **mocr** | Manga OCR ozel modeli |
| **paddleocr** | PaddleOCR motoru |

---

## Gorsel Isleme

### Onarim Modelleri

| Model | Aciklama |
|-------|----------|
| **lama_large** | Buyuk LaMa onarim modeli (onerilen, en iyi etki) |
| **lama_mpe** | LaMa MPE onarim modeli (hizli) |
| **default** | AOT onaricisi (varsayilan) |

### Super Cozunurluk

| Ozellik | Aciklama |
|---------|----------|
| **waifu2x** | Waifu2x super cozunurluk modeli (klasik model) |
| **realcugan** | Real-CUGAN super cozunurluk modeli (onerilen, daha iyi etki, guclu gurultu azaltma) |
| **Super Cozunurluk Katsayisi** | 2x, 3x, 4x buyutmeyi destekler |
| **Real-CUGAN Modeli** | Bircok onceden egitilmis model: muhafazakar, gurultu azaltma yok, 1x/2x/3x gurultu azaltma, Pro surumu |
| **Bolum Isleme** | Buyuk gorsel bolum islemeyi destekler; VRAM kullanimini azaltir |
| **Super Cozunurlugu Geri Al** | Ceviri sonrasi orijinal cozunurlige don (gorsel buyumesini onler) |

**Real-CUGAN Ozellikleri**:
- Yuksek Kaliteli Buyutme: Derin ogrenme tabanli super cozunurluk algoritmasi
- Cok Katmanli Gurultu Azaltma: Gurultu azaltma yok, 1x/2x/3x, muhafazakar mod destekler
- VRAM Dostu: Buyuk gorselleri bolumler halinde isler; VRAM yetersizligini onler
- Pro Surumu: Daha yuksek kaliteli super cozunurluk etkisi saglar

### Renklendirici

| Ozellik | Aciklama |
|---------|----------|
| **none** | Renklendirme yapilmaz (varsayilan) |
| **Diger Renklendirme Modelleri** | Opsiyonel renklendirme ozelligi |

---

## Yazi Tipi Ayarlari

Program `fonts` dizinindeki tum yazi tipi dosyalarini otomatik yukler.

**Ozel Yazi Tipi Ekleme**: [Ayarlar - Nasil Ozel Yazi Tipi Eklenir](SETTINGS.md)

---

## Yuksek Kaliteli Ceviri Ipucu

Ceviri tarzi ve terimlerini optimize etmek icin ozel ipucu destekler.

**Ozel Ipucu Ekleme**: [Ayarlar - Nasil Yuksek Kaliteli Ipucu Eklenir](SETTINGS.md)