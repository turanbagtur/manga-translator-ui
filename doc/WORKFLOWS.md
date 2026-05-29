# Is Akisi Aciklamasi

Bu belge programin 7 is akisini ve ilgili ozelliklerini tanitir.

---

## Ceviri Is Akisi Modu

Program "Ceviri Is Akisi Modu" acilir menusunde 8 is akisi sunar:

---

## 1. Normal Ceviri Is Akisi (Varsayilan)

**Amac**: Gorselleri dogrudan cevir

**Adimlar**:
1. Gorsel dosyalari veya klasoru ekle
2. Cevirici ve hedef dili sec
3. "Ceviriyi Basla" dugmesine tikla
4. Ceviri tamamlaninca sonuclar cikti klasorune kaydedilir

---

## 2. Ceviriyi Disa Aktar

**Amac**: Ceviriden sonra ceviri sonuclarini TXT dosyasina aktar

**Adimlar**:
1. "Ceviriyi Disa Aktar" modunu sec
2. "Gorsel Duzenlenebilir" secenegini isaretle (JSON dosyasi otomatik olusturulur)
3. Ceviriyi basla
4. Program sunlari yapar:
   - Gorseli tam olarak cevir
   - `_translations.json` dosyasi olustur
   - `_translated.txt` dosyasi olustur (ceviri sonuclarini icerir)

---

## 3. Orijinali Disa Aktar

**Amac**: Yalnizca metin algilar ve tanir; orijinali TXT dosyasina aktar; ceviri yapilmaz

**Adimlar**:
1. "Orijinali Disa Aktar" modunu sec
2. "Gorsel Duzenlenebilir" secenegini isaretle (JSON dosyasi otomatik olusturulur)
3. "Yalnizca Orijinal Sablon Olustur" dugmesine tikla
4. Program sunlari yapar:
   - Metin bolgelerini algilar
   - OCR ile orijinali tanir
   - `_translations.json` dosyasi olusturur
   - `_original.txt` dosyasi olusturur (orijinal metni icerir)
   - **Ceviri yapilmaz**, dogrudan durur

**Sonraki Manuel Ceviri**:
1. `manga_translator_work/originals/gorsel-adi_original.txt` dosyasini ac
2. Orijinali hedef dile cevir
3. **Dogrudan `_original.txt` dosyasini degistir** (veya JSON dosyasindaki `translation` alanini degistir)

**TXT Dosya Onceligi** ("Ceviriyi Ice Al ve Olustur" modunda):
- **Once `_original.txt` kullanilir** (orijinal dosya; manuel ceviri sonrasi ice aktarma icin) - En Yuksek Oncelik
- Yoksa `_translated.txt` kullanilir (ceviri dosyasi)
- Her ikisi de yoksa JSON dosyasindaki ceviri dogrudan kullanilir

---

## 4. Ceviriyi Ice Al ve Olustur

**Amac**: TXT veya JSON dosyasindan ceviri icerigi ice al; gorseli yeniden olustur; ceviri yapilmaz

**Adimlar**:
1. "Ceviriyi Ice Al ve Olustur" modunu sec
2. Onceden cevrilmis gorselleri ekle (karsilik gelen `_translations.json` dosyasinin olmasi gerekir)
3. "Ceviriyi Ice Al ve Olustur" dugmesine tikla
4. Program sunlari yapar:
   - **On Isleme**: `_translated.txt` veya `_original.txt` dosyasi varsa once TXT icerigi JSON dosyasina aktar
   - **Ceviriyi Yukle**: JSON dosyasindan ceviri icerigi yukle
   - **Gorseli Olustur**: Yuklenen ceviri icerigi ile gorseli olustur
   - **Ceviri yapilmaz**, dogrudan olusturulur

**TXT Dosya Ice Aktarma Onceligi**:
- **Once `_original.txt` kullanilir** (orijinal dosya; manuel ceviri sonrasi ice aktarma icin) - En Yuksek Oncelik
  - Konum: `manga_translator_work/originals/gorsel-adi_original.txt`
  - Aciklama: Bu dosyadaki orijinal icerigi el ile cevrilmis icerikle degistir
- Yoksa `_translated.txt` kullanilir (ceviri dosyasi)
  - Konum: `manga_translator_work/translations/gorsel-adi_translated.txt`
- Her ikisi de yoksa JSON dosyasindaki ceviri dogrudan kullanilir

**Kullanim Senaryolari**:
- TXT dosyasindaki ceviri icerigi degistirildi; ice aktarip yeniden olusturulacak
- JSON dosyasindaki ceviri icerigi degistirildi; yeniden olusturulacak
- Olusturma parametreleri degistirildi (yazi tipi, renk, dizim vb.); yeniden olusturulacak

---

## 5. Yalnizca Renklendirme (Colorize Only)

**Amac**: Yalnizca siyah-beyaz gorseli renklendir; metin algilama ve ceviri yapilmaz

**Adimlar**:
1. "Yalnizca Renklendirme" modunu sec
2. "Gelismis Ayarlar"da renklendirme parametrelerini yapilandir:
   - **Renklendirme Modeli**: Renklendirici turunu sec
   - **Renklendirme Boyutu**: Isleme boyutunu ayarla
   - **Gurultu Azaltma Yogunlugu**: Gurultu azaltma derecesini kontrol et
3. "Ceviriyi Basla" dugmesine tikla
4. Program sunlari yapar:
   - **Metin algilamayi atlar**
   - **OCR tanımasini atlar**
   - **Ceviriyi atlar**
   - **Yalnizca renklendirme islemini yapar**
   - Renklendirilen gorseli kaydeder

**Kullanim Senaryolari**:
- Siyah-beyaz mangalara renk ekle
- Yalnizca renklendirme; ceviri gerekmiyor

---

## 6. Yalnizca Super Cozunurluk (Upscale Only)

**Amac**: Yalnizca gorsele super cozunurluk islemi uygula; metin algilama ve ceviri yapilmaz

**Adimlar**:
1. "Yalnizca Super Cozunurluk" modunu sec
2. "Gelismis Ayarlar"da super cozunurluk parametrelerini yapilandir:
   - **Super Cozunurluk Modeli**: `waifu2x`, `realcugan` (onerilen) veya `mangajanai` (en iyi etki) sec
   - **Super Cozunurluk Katsayisi**: 2x, 3x veya 4x sec
   - **Real-CUGAN Modeli**: Uygun onceden egitilmis modeli sec (ornegin `3x-denoise3x`)
   - **Bolum Boyutu**: VRAM yetersizse bolum boyutunu ayarla (ornegin 400)
3. "Ceviriyi Basla" dugmesine tikla
4. Program sunlari yapar:
   - **Metin algilamayi atlar**
   - **OCR tanimasini atlar**
   - **Ceviriyi atlar**
   - **Yalnizca super cozunurluk islemini yapar**
   - Buyutulmus gorseli kaydeder

**Kullanim Senaryolari**:
- Gorsel cozunurluğunu arttirir; ceviri gerekmiyor
- Dusuk cozunurluklu manga gorsellerini buyutme
- Gorsel gurultu azaltma (Real-CUGAN gurultu azaltma modeli kullanarak)

**Onerilen Yapilandirma**:
- **Yuksek Kaliteli Buyutme**: `realcugan` + `3x-denoise3x` veya `3x-denoise3x-pro`
- **En Iyi Etki**: `mangajanai` (en iyi modeli otomatik secer)
- **Hizli Buyutme**: `waifu2x` + 2x/3x/4x
- **VRAM Yetersizliginde**: `tile_size=400` ayarla (veya daha kucuk)

---

## 7. Yalnizca Onarim (Inpaint Only)

**Amac**: Yalnizca metni algilar ve siler (gorseli onarir); ceviri ve olusturma yapilmaz; temiz gorsel ciktisi verir

**Adimlar**:
1. "Yalnizca Onarim" modunu sec
2. "Gelismis Ayarlar"da onarim parametrelerini yapilandir:
   - **Onarim Modeli**: `lama_large` (onerilen) veya `lama_mpe` sec
   - **Onarim Boyutu**: Isleme boyutunu ayarla
   - **Onarim Hassasiyeti**: `fp32`, `fp16` veya `bf16` sec
3. "Onarimi Basla" dugmesine tikla
4. Program sunlari yapar:
   - **Metin bolgelerini algilar**
   - **Metin maskesi olusturur**
   - **Gorsel onarimı yapar** (metni siler)
   - **Ceviriyi atlar**
   - **Olusturmayi atlar**
   - Metni silinmis temiz gorseli kaydeder

**Kullanim Senaryolari**:
- Metinsiz temiz manga gorseli elde etme
- Sonraki manuel duzenleme icin malzeme hazirlama
- Gorsellerden yazi damgalarini kaldir
- Diger araclarla ikincil yaraticilik icin

**Cikti Dosyalari**:
- Onarilmis gorsel cikti klasorune kaydedilir
- Dosya adi bicimi: `orijinal-dosya-adi_inpainted.png`

**Onerilen Yapilandirma**:
- **Yuksek Kaliteli Onarim**: `lama_large` + `fp32` veya `bf16`
- **Hizli Onarim**: `lama_mpe` + `fp16`
- **VRAM Yetersizliginde**: "Onarim Boyutu" parametresini dusurun

---

## 8. Ceviriyi Degistir (Replace Translation)

**Amac**: Cevrilmis gorselden ceviri verilerini cikar ve orijinal gorsele uygula; ceviri yapilmis gorseli yeniden islemek gerektiginde uygundur

**On Kosullar**:
- Orijinal gorsel ve karsilik gelen cevrilmis gorsel hazirlanmis olmalidir
- Orijinal gorsel ile cevrilmis gorsel dosya adlari karsilik gelmeli (ornegin: `page1.jpg` ve `page1.jpg`)
- Cevrilmis gorsel `orijinal-gorsel-dizini/manga_translator_work/translated_images/` altinda olmalidir

**Adimlar**:
1. Dosya yapisini hazirla:
   ```
   orijinal-gorsel-dizini/
   |-- page1.jpg                              # Orijinal gorsel
   |-- page2.jpg
   `-- manga_translator_work/
       `-- translated_images/                 # Cevrilmis gorsel klasoru
           |-- page1.jpg                      # Karsilik gelen cevrilmis gorsel (ayni dosya adi)
           `-- page2.jpg
   ```

2. Arayuzde "Ceviriyi Degistir" secenegini isaretle

3. Orijinal gorselleri ekle (`page1.jpg`, `page2.jpg` vb.)

4. "Ceviriyi Basla" dugmesine tikla

5. Program sunlari yapar:
   - **Cevrilmis gorsellerden OCR sonuclarini cikar** (cevirilmis metni tanir)
   - **Orijinal gorsellerden OCR sonuclarini cikar** (orijinal metni tanir)
   - **Bolgeleri otomatik eslestirir** (konuma ve cakisma oranina gore)
   - **Maske optimizasyonu ve onarimi yapar** (orijinal gorseldeki metni siler)
   - **Ceviri metnini olusturur** (cevrilmis gorseldeki yaziyi orijinal gorsele olusturur)
   - **Sonucu kaydeder**

**Eslestirme Mantigi**:
- Orijinal kutu ile cevrilmis kutunun cakisma oranini hesaplar (kucuk kutu esas alinir)
- Cakisma >= %30 ise eslestirme basarili sayilir
- Cok-bire eslestirme destekler (birden fazla orijinal kutu bir cevrilmis kutuya karsilik gelir)
- Eslestirme basarisiz alanlar gunlukte uyari olarak gosterilir

**Kullanim Senaryolari**:
- Cevrilmis gorsel mevcut; ancak orijinal yeniden islenecek
- Ceviri icerigi degistirilecek; mevcut ceviri sonucu korunacak
- Baska ceviri aracindan bu programa gec
- Mevcut ceviri verilerini toplu olarak uygula

**Avantajlari**:
- Yeniden ceviri gerekmez; API harcamalari azalir
- Orijinal ceviri kalitesi korunur
- Optimize edilmis maske otomatik kaydedilir; Qt duzenleyicisi yuklerken maske optimizasyonu atlar
- Duzenlenebilir PSD dosyasi disa aktarmayi destekler

**Dikkat Edilecekler**:
- Paralel isleme desteklenmez (otomatik siralı isleme kullanilir)
- Orijinal gorsel ile cevrilmis gorsel cozunurlukleri ayni veya benzer olmalidir
- Cevrilmis gorsel `manga_translator_work/translated_images/` altinda olmalidir
- Cevrilmis gorsel dosya adi orijinal gorsel ile ayni olmalidir (uzanti farkli olabilir)
- Eslestirme basarisizsa dosya adlarinin karsilik gelip gelmedgini kontrol edin

---

## Gorsel Duzenlenebilir Secenegi

**Islevi**: Isaretlendiginde program `_translations.json` dosyasi olusturur; bu dosya sunlari icerir:
- Algilanan metin bolgeleri
- OCR ile tanınan orijinal metin
- Ceviri sonuclari
- Metin kutusu konum bilgisi

**Kullanim Amaci**:
- Ceviri icerigi sonradan kolayca degistirilebilir
- Gorsel, duzenleyicide acilarak gorsel duzenleme yapilabilir
- "Ceviriyi Ice Al ve Olustur" moduyla yeniden olusturulabilir

---

## AI Satir Sonu Ozelligi

**Desteklenen Aralik**: OpenAI, Gemini ceviricilerini destekler (yuksek kalite modu dahil)

**Islevi**: Akilli AI satir sonu kullanir; metin satir sonlarini otomatik optimize eder

**Calisma Prensibi**:
- Ceviri isteğine `[Original regions: X]` on eki ekler
- AI'a orijinal metnin kac metin bolgesi icerdigini bildirir
- AI orijinal bolge sayisina gore akilli satir sonu uygular
- **API cagri sayisini artirmaz**; yalnizca ayni cagridaki ek bilgidir

**Etkinlestirme Yontemi**:
1. Desteklenen ceviriciyi sec (OpenAI, Gemini, Yuksek Kaliteli OpenAI, Yuksek Kaliteli Gemini)
2. Olusturma ayarlarinda "AI Satir Sonu" secenegini isaretle
3. Ceviriyi basla

---

## Yeni Terim Otomatik Cikarma Ozelligi

**Desteklenen Aralik**: OpenAI, Gemini ceviricilerini destekler (yuksek kalite modu dahil)

**Islevi**: Ceviri sonuclarindan ozgun isimleri (kisi adlari, yer adlari, organizasyon adlari vb.) otomatik cikarir ve terim listesine ekler; sonraki cevirilerde tutarliligi saglar

**Calisma Prensibi**:
1. **Ceviri Asamasi**: AI ceviri yaparken orijinal metindeki ozgun isimleri tanimlar
2. **Cikarma Asamasi**: Ceviri tamamlaninca AI tanidigi terimleri ve cevirilerini otomatik cikarir
3. **Kaydetme Asamasi**: Cikarilan terimler mevcut ipucu dosyasinin `glossary` alanina otomatik eklenir
4. **Uygulama Asamasi**: Sonraki cevirilerde AI terim listesine basvurur; ceviri tutarliligini korur

**Terim Kategorileri**:
- **Person**: Kisi adlari (karakter adlari, yazar adlari vb.)
- **Location**: Yer adlari (sehir, ulke, kurgusal yerler vb.)
- **Org**: Organizasyon adlari (sirket, okul, grup vb.)
- **Item**: Nesne adlari (alet, ekipman, esya vb.)
- **Skill**: Yetenek adlari (buyul, hareket, kabiliyet vb.)
- **Creature**: Varlik adlari (canavar, irk, hayvan vb.)

**Etkinlestirme Yontemi**:
1. Desteklenen ceviriciyi sec
2. "Temel Ayarlar"da ozel ipucu dosyasi sec veya olustur
3. "Yeni Terimi Otomatik Cikar" secenegini isaretle
4. Ceviriyi basla

**Kullanim Senaryolari**:
- **Uzun Manga Suruklu Ceviri**: Terim listesini otomatik biriktirir; karakter adi gibi ozgun isimlerin tutarliligini saglar
- **Seri Eser Cevirisi**: Ayni ipucu dosyasinda terimleri biriktirir; eserlerde tutarliligi korur
- **Takim Isbirligi**: Ipucu dosyasini paylas; ceviri standartlarini birlestir

---

## Ozel Orijinal Disa Aktarma Sablonu

**Amaci**: Harici araclarla ceviri kolaylastirmak icin orijinal disa aktarma bicimini ozellestir

**Sablon Dosya Konumu**: `examples/translation_template.json`

**Calisma Prensibi**:
- Sablon **bir grup metin kutusu** bicimini tanimlar
- Disa aktarirken program sablon girislerinin sayisina gore gruplara ayirir
- **Tekrarlanan metin kutusu bolumuudur**; tum JSON yapisi degil
- Ornek: Sablonda 3 yer tutucu cift varsa her 3 metin kutusu bir grup olarak cikarilir

**Kullanim Talimatlari**:
1. `examples/translation_template.json` dosyasini duzenle
2. Bir grup metin kutusunun bicimini tanimla (1, 3 veya istenen sayi)
3. `<original>` ve `<translated>` yer tutucularini kullan
4. Orijinali disa aktarirken her grup metin kutusu bu bicimi yeniden kullanir
5. Manuel ceviri sonrasi "Ceviriyi Ice Al ve Olustur" islevi ile ice aktar

---

## Calisma Dosyasi Yollari (Otomatik Olusturulur)

Program gorsel dizininde `manga_translator_work` klasoru olusturur:

- **JSON Dosyasi**: `manga_translator_work/json/gorsel-adi_translations.json`
  - Metin bolgeleri, orijinal, ceviri, konum bilgisi icerir

- **Orijinal TXT**: `manga_translator_work/originals/gorsel-adi_original.txt`
  - Orijinal disa aktarimda olusturulur

- **Ceviri TXT**: `manga_translator_work/translations/gorsel-adi_translated.txt`
  - Manuel ceviri sonrasi burada kaydedilir

- **Onarilmis Gorsel**: `manga_translator_work/inpainted/gorsel-adi_inpainted.png`
  - Metin silinmis gorsel
  - Qt duzenleyicisi yuklemesi ve duzenleme icin kullanilir

- **Ceviri Sonucu**: `manga_translator_work/result/gorsel-adi.png`
  - "Ciktiyi Orijinal Gorsel Dizinine Kaydet" etkinlestirildiginde buraya ciktı verilir

- **PSD Dosyasi**: `manga_translator_work/psd/gorsel-adi.psd`
  - "Duzenlenebilir PSD Disa Aktar" etkinlestirildiginde katmanli PSD dosyasi disa aktarilir

- **Cevrilmis Gorsel**: `manga_translator_work/translated_images/gorsel-adi.jpg`
  - Ceviriyi Degistir modu: cevrilmis gorselleri buraya koy