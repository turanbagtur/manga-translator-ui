# Kullanim Kilavuzu

Bu belge programin temel kullanim yontemlerini ve yaygin ayarlari aciklamaktadir.

---

## Icindekiler

- [Ilk Kullanim](#ilk-kullanim)
- [Temel Islemler](#temel-islemler)
- [Cevirici Secimi](#cevirici-secimi)
- [Yaygin Ayarlar](#yaygin-ayarlar)
- [Gorsel Duzenleyici](#gorsel-duzenleyici)
- [Sik Sorulan Sorular](#sik-sorulan-sorular)

---

## Ilk Kullanim

### 1. Model Dosyalarini Indirme (Istege Bagli)

Ilk calistirmada model otomatik indirimesi basarisiz olursa veya cok yavas indiriyorsa, model dosyalarini elle indirebilirsiniz:

**Model Dosyalari Bulut Depolama:**

- **Quark Disk**:
  - Baglanti: https://pan.quark.cn/s/e4e8d1635bf1
  - Kod: `e77d39EiKf`

- **Baidu Disk**:
  - Baglanti: https://pan.baidu.com/s/17YIs2nvgUAapcTI1i0ncFA?pwd=3w3u
  - Kod: `3w3u`

**Indirdikten Sonra Kullanim:**
1. `models` klasorunu indirin
2. `models` klasorunu programin kok dizinine koyun (`app.exe` veya `Adim2-QtArayuzuBaslat.bat` ile ayni dizin)
3. Programi baslatin

> Program model otomatik indirimesini basarili yapiyorsa elle indirmeye gerek yoktur.

### 2. Programi Baslatin

Kurulum yonteminize gore baslangic yontemini secin:

**Betik Kurulum Surumu**:
- `Adim2-QtArayuzuBaslat.bat` dosyasina cift tiklayin

**Paketlenmis Surum**:
- `app.exe` dosyasina cift tiklayin

**Manuel Dagitim Surumu**:
- Komutu calistirin: `py -3.12 -m desktop_qt_ui.main`

Ilk calistirmada:
- AI modelleri otomatik yuklenir (3-5 dakika surer)
- Ceviri motoru baslatilir
- Ana arayuz acilir

### 3. CPU Surumu Icin Zorunlu Ayarlar

**CPU surumu** kullaniyorsaniz veya NVIDIA ekran kartiniz yoksa:

1. "**Temel Ayarlar**" sekmesine tiklayin
2. **"GPU Kullan" seceneginin isaretini kaldilin**
3. "**Yapilandirmayi Kaydet**" dugmesine tiklayin

> CPU surumunda veya NVIDIA ekran karti yokken GPU etkinlestirmek programa cokmasina neden olur!

### 4. Cikti Dizinini Ayarlama

1. Ana arayuzde "**Cikti Klasoru Sec**" dugmesine tiklayin
2. Ceviri sonuclarinin kaydedilecegi konumu secin
3. Program bu ayari otomatik hatirlar

---

## Temel Islemler

### Gorsel Ekleme

Uc yontem desteklenmektedir:

1. **Dosya Ekle Dugmesine Tiklayin**:
   - "Dosya Ekle" dugmesine tiklayin
   - Bir veya birden fazla gorsel dosyasi secin

2. **Tum Klasoru Ekleyin**:
   - "Klasor Ekle" dugmesine tiklayin
   - Gorsel iceren klasoru secin
   - Program tum gorselleri otomatik tarar

3. **Surukleyip Birakın** (en kolay):
   - Gorsel veya klasorleri dogrudan pencereye surukleyin
   - Birden fazla dosya/klasor ayni anda suruklenebilir

**Desteklenen Gorsel Formatlari**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`

### Cevirici Secimi

1. "**Temel Ayarlar**" sekmesinde "**Cevirici**" acilir menusunu bulun
2. Ilk kullanim icin onerilen:
   - **Yuksek Kaliteli OpenAI** veya **Yuksek Kaliteli Gemini** (cok modlu, gorsel ceviri, en iyi sonuc) - Kesinlikle Onerilen
   - **OpenAI** veya **Gemini** (duz metin cevirisi, API yapilandirmasi gerektirir)

> Onemli Not:
> - **Yuksek Kaliteli Ceviriciler** cok modlu modeli destekleyen modeller gerektirir (GPT-4o, Gemini gibi)
> - DeepSeek gibi modeller cok modali desteklemez; **Yuksek Kaliteli Cevirici kullanilamaz**, standart cevirici secin
> - Cevrimici ceviriciler API Key yapilandirmasi gerektirir -> [API Yapilandirma Kilavuzu](API_CONFIG.md)

### Hedef Dil Secimi

1. "**Temel Ayarlar**"da "**Hedef Dil**" acilir menusunu bulun
2. Yaygin secimler:
   - **Turkce** (TUR)
   - **Basitlestirilmis Cince** (CHS)
   - **Ingilizce** (ENG)

### Ceviriyi Baslatin

1. Ayarlarinizi dogrulayin:
   - GPU ayari dogru (CPU surumunda kapali olmali)
   - Cikti klasoru secilmis
   - Gorsel eklenmis
   - Cevirici ve hedef dil secilmis

2. "**Ceviriyi Basla**" dugmesine tiklayin

3. Ceviri tamamlanmasini bekleyin:
   - Ilerleme cubugu ceviri ilerlemesini gosterir
   - Gunluk penceresi ayrintili bilgi gosterir
   - Istediginiz zaman "Durdur" dugmesine tiklayarak ceviriyi kesebilirsiniz

4. Sonuclari inceleyin:
   - Ceviri tamamlandiktan sonra sonuclar otomatik cikti klasorune kaydedilir
   - Dosya adi bicimi: `orijinal-dosya-adi_translated.jpg`

---

## Cevirici Secimi

### Cevrimici Ceviriciler (API Key Gerektirir)

| Cevirici | Ozellikler | Ucret | Kalite | Yapilandirma Zorlugu |
|----------|------------|-------|--------|----------------------|
| **OpenAI** | GPT serisi modeller | Orta | Yuksek | Kolay |
| **Gemini** | Google AI | Dusuk | Yuksek | Kolay |
| **Sakura** | Japonca optimizasyonu | Orta | Yuksek | Orta |

### Yuksek Kaliteli Ceviriciler (Kesinlikle Onerilen)

Cok modlu AI modelini kullanir; gorsel baglaminla birlikte ceviri yapar:

| Cevirici | Ozellikler | Avantaj | Oneri |
|----------|------------|---------|-------|
| **Yuksek Kaliteli OpenAI** | GPT-4o | Gorsel ceviri, baglamı anlar | ***** |
| **OpenAI** | GPT-4o | Duz metin cevirisi | **** |
| **Yuksek Kaliteli Gemini** | Gemini | Gorsel ceviri, hizli | ***** |
| **Gemini** | Gemini | Duz metin cevirisi | **** |

**Yuksek Kaliteli Ceviricilerin Avantajlari**:
- Cok Modlu Anlama: AI gorsel icerigi "gorebilir" ve sahneyi anlar
- Daha Dogru: Gorsel bilgiyle birlestirilmis, baglama daha uygun ceviri
- Toplu Isleme: Bir seferde birden fazla gorsel gonderilir; AI genel konuyu anlar
- Ozel Ipucu: Ozel ceviri tarzini ve terim listesini destekler -> [Nasil Ipucu Eklenir](SETTINGS.md)

### Cevrimici Ceviriciyi Yapilandirma

API Key gerektiren ceviriciler icin ayrintili yapilandirma kilavuzuna bakin:

**API Yapilandirma Kilavuzu** -> [API_CONFIG.md](API_CONFIG.md)

**Onerilen Yapilandirma**:
- En Iyi Sonuc: OpenAI GPT-4o veya Google Gemini (cok modlu modeller)

---

## Yaygin Ayarlar

### Ceviri Is Akisi Modu

Program "**Ceviri Is Akisi Modu**" acilir menusunde 8 is akisi sunar:

1. **Normal Ceviri Is Akisi** (varsayilan):
   - Gorsel dogrudan cevrilir, ceviri sonucu uretilir

2. **Ceviriyi Disa Aktar**:
   - Ceviriden sonra sonuclari TXT dosyasina aktar
   - Sonraki duzenleme icin uygun

3. **Orijinali Disa Aktar**:
   - Yalnizca metin algila ve tani, orijinali TXT'ye aktar
   - Ceviri yapilmaz; manuel ceviri icin kullanilir

4. **Ceviriyi Ice Al ve Olustur**:
   - TXT/JSON dosyasindan ceviri icerigi ice al
   - Gorseli yeniden olustur (ceviri yapilmaz)

5. **Yalnizca Renklendirme**:
   - Yalnizca siyah-beyaz gorseli renklendir
   - Metin algilama ve ceviri yapilmaz

6. **Yalnizca Super Cozunurluk**:
   - Yalnizca gorsel super cozunurluk islemi uygula
   - Metin algilama ve ceviri yapilmaz

7. **Yalnizca Onarim**:
   - Yalnizca metin algilar ve siler (gorsel onarm)
   - Ceviri ve olusturma yapilmaz; temiz gorsel ciktilar

8. **Ceviriyi Degistir**:
   - Cevrilmis gorselden ceviri verilerini cikar ve orijinal gorsele uygula

**Ayrintili Is Akisi Aciklamasi** -> [Is Akislari](WORKFLOWS.md)

### OCR Modeli Secimi

"**Secenekler**" sekmesinden OCR modeli secin:

- **48px** (onerilen): Varsayilan model, hiz ve dogruluk dengesi
- **48px_ctc**: CTC modeli, daha yuksek tanima dogrulugu
- **mocr**: Manga OCR ozel modeli
- **paddleocr**: PaddleOCR motoru, cok dil destegi

### Yazi Tipi Ayarlari

Program `fonts` dizinindeki tum yazi tiplerini otomatik yukler.

**Ozel Yazi Tipi Ekleme**: [Ayarlar - Nasil Ozel Yazi Tipi Eklenir](SETTINGS.md)

### Filtre Listesi (Su Damgasini/Reklamlari Atla)

Program filtre listesi araciligiyla belirli metin bolgelerini atlamayı destekler; su damgasi, reklam gibi cevrilmesi gerekmeyen icerikleri filtrelemek icin yaygin olarak kullanilir.

**Dosya Konumu**: `examples/filter_list.txt`

**Kullanim Yontemi**:
1. Ayarlar panelinde "**Filtre Listesini Ac**" dugmesine tiklayin
2. Ilgili bolume filtre kelimelerini ekleyin (buyuk/kucuk harf duyarsiz)
3. `#` ile baslayan satirlar yorum satiridir
4. Dosyayi kaydettikten sonra bir sonraki ceviride otomatik gecerli olur

**Iki Filtre Modu**:
- `[Iceren Filtre]`: Orijinal metin bu metinleri **iceriyorsa** filtrele (bulanik eslestirme)
- `[Kesin Filtre]`: Orijinal metin bu metinlerle **tamamen eslesiyorsa** filtrele (kesin eslestirme)

**Ornek**:
```
[Iceren Filtre]
# Orijinal bu metinleri iceriyorsa filtrele
pixiv
twitter

[Kesin Filtre]
# Orijinal bu metinlerle tamamen eslesiyorsa filtrele
v.com
©
```

---

## Gorsel Duzenleyici

Ceviri tamamlandiktan sonra sonuclari degistirmek istiyorsaniz:

### Duzenleyiciyi Acin

1. Cevirinin "**Gorsel Duzenlenebilir**" secenegiyle yapildigini dogrulayin
2. Ceviri tamamlandiktan sonra ana arayuzde "**Duzenleyiciyi Ac**" dugmesine tiklayin
3. Duzenlenmek istenen gorseli secin (karsilik gelen `_translations.json` dosyasinin olmasi gerekir)

### Duzenleme Islemleri

Duzenleyici zengin duzenleme ozellikleri sunar:

- **Alan Duzenleme**:
  - Tasima: Metin kutusunu surukle
  - Dondurme: Dondurme tutamacini kullan
  - Sekil Degistirme: Metin kutusu koselerini gerin

- **Metin Duzenleme**:
  - Ceviriyi degistirmek icin metin kutusuna cift tiklayin
  - Sag taraftaki ozellik panelinden yazi tipi, boyut ve rengi ayarlayin
  - Yatay/Dikey metni degistirin

- **Maske Duzenleme**:
  - Firca araci ile metin silme bolgesi elle cizin
  - Hatalari duzeltmek icin silgiyi kullanin

- **Yaygin Kisayol Tuslari**:
  - **Arac Degistirme**:
    - `Q`: Secim araci
    - `W`: Firca araci
    - `E`: Silgi araci
  - **Dosya Islemleri**:
    - `Ctrl+Q`: Gorseli disa aktar
    - `Ctrl+W`: JSON kaydet
    - `Ctrl+E`: Orijinal gorseli duzenle
  - **Gorsel Gezintisi**:
    - `A`: Onceki gorsel
    - `D`: Sonraki gorsel
  - **Gecmis**:
    - `Ctrl+Z`: Geri al
    - `Ctrl+Y`: Yeniden yap
  - **Fare Tekeri Kisayollari**:
    - `Ctrl + Tekerlek`: Secili metin kutusunu orantili olarak yeniden boyutlandir
    - `Shift + Tekerlek`: Maske firca boyutunu ayarla
    - `Tekerlek`: Gorseli yakınlaştir/uzaklastir

**Ayrintili Duzenleme Ozellikleri** -> [Ozellikler](FEATURES.md)

---

## Sik Sorulan Sorular

### S1: Ceviri hizi cok yavas; ne yapabilirim?

**Olasi Nedenler ve Cozumler**:
1. **CPU ile Ceviri Yapiyorsunuz**:
   - CPU surumu GPU surumundan 5-10 kat daha yavas
   - GPU surumunu kullanmaniz onerilir (NVIDIA ekran karti gerektirir)

2. **Gorsel Cozunurlugu Cok Yuksek**:
   - "**Gelismis Ayarlar**"da "**Algilama Boyutu**"nu dusurun (varsayilan 2048)
   - "**Onarim Boyutu**"nu dusurun

### S2: Ceviri sonuclari dogru degil; ne yapabilirim?

**Cozumler**:
1. **Ceviriciyi Degistirin**:
   - Yuksek Kaliteli Cevirici deneyin (OpenAI HQ, Gemini HQ)

2. **Manuel Ceviri Kullanın**:
   - "**Orijinali Disa Aktar**" is akisini secin
   - Orijinali elle ceevirin
   - "**Ceviriyi Ice Al ve Olustur**" ile yeniden olusturun

3. **Duzenleyiciyi Kullanin**:
   - "**Gorsel Duzenlenebilir**" secenegini isaretleyin
   - Ceviri tamamlandiktan sonra duzenleyiciyi acin
   - Ceviriyi elle degistirin

### S3: Tum metinler algilanmiyor; ne yapabilirim?

**Cozumler**:
1. **Ayrintili Gunluk Acin**:
   - "**Temel Ayarlar**"da "**Ayrintili Gunluk**" secenegini isaretleyin
   - `result/` dizinindeki hata ayiklama dosyalarini inceleyin

2. **Algilama Parametrelerini Ayarlayin**:
   - "**Gelismis Ayarlar**"da "**Metin Esik Degeri**"ni dusurun (varsayilan 0.5)
   - "**Sinir Kutusu Esigi**"ni dusurun
   - "**Unclip Oranini**" artirin (varsayilan 2.5)

3. **Duzenleyici ile Elle Ekleyin**:
   - Duzenleyicide "Sekil Duzenle" dugmesine tiklayin
   - Algilanmayan metin bolgelerini elle secin

**Ayrintili Hata Ayiklama Yontemi** -> [Hata Ayiklama Kilavuzu](DEBUGGING.md)

### S4: GPU surumu cokuyor; ne yapabilirim?

**Cozumler**:
1. **Ekran Karti Uyumluluğunu Kontrol Edin**:
   - Ekran kartinin CUDA 12.x destekleyip desteklemedigini dogrulayin
   - GTX 1060 ve uzeri onerilir

2. **Surucu Guncelleyin**:
   - NVIDIA ekran karti surucusunu kurun veya guncelleyin
   - [CUDA Toolkit 12.x](https://developer.nvidia.com/cuda-downloads) kurun

3. **CPU Surumuna Gecin**:
   - "**GPU Kullan**" seceneginin isaretini kaldilin
   - Veya CPU surumu programi indirin

### S5: Tum klasoru toplu olarak nasil ceviririm?

**Islem Yontemi**:
1. "**Klasor Ekle**" dugmesine tiklayin
2. Gorsel iceren klasoru secin
3. Program tum gorselleri otomatik tarar
4. "**Ceviriyi Basla**" dugmesine tiklayin
5. Tum gorsellerin cevirisinin tamamlanmasini bekleyin

> "**Temel Ayarlar**"da "**Toplu Boyut**"u ayarlayarak ayni anda islenen gorsel sayisini kontrol edebilirsiniz.

---

## Sonraki Adimlar

Daha fazla ozellik ogrenin:
- [Ozellikler](FEATURES.md) - Tum ozellikleri goruntuleyin
- [Is Akislari](WORKFLOWS.md) - Farkli is akislarini ogrenin
- [Ayarlar](SETTINGS.md) - Ayrintili parametre yapilandirmasi
- [Hata Ayiklama Kilavuzu](DEBUGGING.md) - Ceviri sorunlarini cozun

[Ana Sayfa](../README.md)'ya don