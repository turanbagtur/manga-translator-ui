# Ayarlar Kilavuzu

Bu belge programin tum ayar seceneklerini ve parametrelerini ayrintili olarak aciklamaktadir.

---

## Parametre Aciklamalari

Arayuz uc sekmeden olusur; her sekme farkli ayar secenekleri icerir:

---

## Temel Ayarlar

### Cevirici Ayarlari

- **Cevirici (translator)**: Ceviri motorunu sec
  - Cevrimici ceviriciler: Google Gemini, OpenAI, DeepL vb.
  - Yuksek kaliteli ceviriciler: Yuksek Kaliteli OpenAI, Yuksek Kaliteli Gemini (onerilen)

- **Hedef Dil (target_lang)**: Cevirinin hedef dili
  - Basitlestirilmis Cince, Geleneksel Cince, Ingilizce, Japonca, Korece, Turkce vb.

- **Hedef Dil Metnini Atlamayin (no_text_lang_skip)**: Zaten hedef dilde olan metni atlamayin (zorla cevir)

- **Ozel Ipucu (high_quality_prompt_path)**: Ozel ipucu dosya yolu
  - Uygulanabilir: OpenAI, Gemini, Yuksek Kaliteli OpenAI, Yuksek Kaliteli Gemini ceviricileri
  - Varsayilan: `dict/prompt_example.json`
  - `dict` dizinine yeni `.json` dosyasi eklenebilir
  - JSON bicimi standart JSON spesifikasyonuna uygun oldugu surece yuklenebilir
  - Program acilir menu her acilisinda `dict` dizinini otomatik tarar
  - Yeni ipucu dosyasi eklendikten sonra yeniden baslatmaya gerek yok; acilir menuye tiklayin

- **Yeni Terimi Otomatik Cikar (extract_glossary)**: Ceviri sonuclarindan yeni terim otomatik cikar
  - Uygulanabilir: OpenAI, Gemini, Yuksek Kaliteli OpenAI, Yuksek Kaliteli Gemini ceviricileri
  - Isaretlenince AI kisi adlari, yer adlari, organizasyon adlari gibi ozgun isimleri otomatik tanimlar ve cikarir
  - Cikarilan terimler ozel ipucu terim listesine otomatik eklenir
  - Sonraki cevirilerde bu terimlere basvurularak tutarlilik korunur
  - Uzun manga surekli cevirisinde ozgun isimlerin tutarliligini saglamak icin idealdir

- **Ozel API Parametresi Kullan (use_custom_api_params)**: Ozel API parametresini etkinlestir
  - Uygulanabilir: OpenAI, OpenAI HQ, Gemini, Gemini HQ ceviricileri
  - Isaretlenince program `examples/custom_api_params.json` dosyasindan ozel parametreleri okur ve API'ye iletir
  - "Dosyayi Ac" dugmesine tiklayarak yapilandirma dosyasini otomatik olustur ve ac
  - Yapilandirma dosyasi standart JSON; her ceviride yeniden yuklenir (canli gecerlilik)
  - Kullanim senaryolari:
    - Ollama gibi yerel modeller icin ozel parametreleri kontrol et (dusunme modunu kapat gibi)
    - API sicaklik, maksimum token sayisi vb. parametrelerini ayarla
    - Modele ozgu yapilandirma seceneklerini ilet
  - Yapilandirma ornegi:
    ```json
    {
      "temperature": 0.7,
      "max_tokens": 2000
    }
    ```
  - DeepSeek dusunme modunu kapatma ornegi:
    ```json
    {
      "thinking": {"type": "disabled"}
    }
    ```
  - Gemini dusunme modunu kapatma ornegi:
    ```json
    {
      "thinking_budget": 0
    }
    ```

- **Maksimum Istek Hizi (max_requests_per_minute)**: Dakika basina maksimum istek sayisi (0 = sinir yok)

### CLI Secenekleri

- **Ayrintili Gunluk (verbose)**: Ayrintili hata ayiklama bilgisi ciktisi

- **GPU Kullan (use_gpu)**: GPU hizlandirmasini etkinlestir

- **Yeniden Deneme Sayisi (attempts)**: Hata yeniden deneme sayisi (-1 = sinirsiz yeniden deneme)

- **Hatalari Yoksay (ignore_errors)**: Hatalari yoksay ve islemeye devam et

- **Baglam Sayfa Sayisi (context_size)**: Ceviri baglamindaki sayfa sayisi (cok sayfalı ortak ceviri icin)

- **Cikti Bicimi (format)**: Cikti gorsel bicimi
  - PNG, JPEG, WEBP, belirtilmemis (orijinal bicimi koru)

- **Mevcut Dosyanin Uzerine Yaz (overwrite)**: Mevcut ceviri dosyasinin uzerine yaz

- **Metinsiz Gorseli Atla (skip_no_text)**: Metin algilanmayan gorseli atla

- **Gorsel Duzenlenebilir (save_text)**: Ceviri sonucunu JSON dosyasina kaydet (sonraki duzenleme icin)

- **Ceviriyi Ice Al (load_text)**: JSON dosyasindan ceviri sonucunu yukle

- **Orijinali Disa Aktar (template)**: Orijinal metni metin dosyasina aktar (manuel ceviri icin)

- **Gorsel Kayit Kalitesi (save_quality)**: JPEG kayit kalitesi (0-100)

- **Toplu Boyut (batch_size)**: Toplu isleme boyutu
  - Varsayilan: 1
  - Yuksek Kaliteli Ceviriciler (OpenAI HQ/Gemini HQ) icin bir seferde gonderilen gorsel sayisini kontrol eder
  - Buyudukce ceviri hizi artar; ancak token tuketimi artar
  - Onerilen aralik: 1-10

- **Toplu Eszamanli Isleme (batch_concurrent)**: Toplu esit zamanli islemeyi etkinlestir

- **Duzenlenebilir PSD Disa Aktar (export_editable_psd)**: Katmanli PSD dosyasi disa aktar
  - Photoshop gerektirir
  - Disa aktarilan: orijinal, onarilmis, duzenlenebilir metin katmani
  - Disa aktarma yolu: `orijinal-gorsel-dizini/manga_translator_work/psd/`

- **PSD Varsayilan Yazi Tipi (psd_font)**: Photoshop'ta goruntulenecek metin katmani yazi tipi

- **Yalnizca PSD Betigini Olustur (psd_script_only)**: Yalnizca .jsx betigi olustur; Photoshop'u otomatik calistirma

- **Ceviri Sonrasi Modeli Kaldir (unload_models_after_translation)**: Ceviri tamamlaninca bellek bosaltmak icin tum modelleri kaldir
  - Varsayilan: Kapali
  - Islevi: VRAM ve bellek daha kapsamli bosaltilir; VRAM yetersizligi durumunda kullanilir
  - Dezavantaj: Bir sonraki ceviride modeller yeniden yuklenmek zorunda kalir

- **Olustur ve Disa Aktar (generate_and_export)**: Ceviri sonucunu olustur ve disa aktar

- **Yalnizca Renklendirme (colorize_only)**: Yalnizca renklendirme uygula; ceviri yapilmaz

- **Yalnizca Super Cozunurluk (upscale_only)**: Yalnizca super cozunurluk islemi uygula; ceviri yapilmaz

- **Ciktıyı Orijinal Gorsel Dizinine Kaydet (save_to_source_dir)**: Ceviri sonucunu orijinal gorsel dizinine cikti ver
  - Etkinlestirilince cikti yolu: `orijinal-gorsel-dizini/manga_translator_work/result/`
  - Cevrilmis gorselleri yonetmek ve bulmak kolaylasir
  - Toplu islemede dosya organizasyon yapisini korumak icin uygundur

- **Ceviriyi Degistir (replace_translation)**: Cevrilmis gorsellerden ceviri verisi cikar ve orijinal gorsele uygula
  - Orijinal ile cevrilmis gorsel metin bolgelerini otomatik eslestir
  - Cok-bire eslestirme destekler
  - Optimize edilmis maske otomatik kaydedilir
  - Duzenlenebilir PSD disa aktarmayi destekler
  - Paralel isleme desteklenmez (otomatik sirali isleme)

---

## Gelismis Ayarlar

### Algilayici Ayarlari

- **Metin Algilayici (detector)**: Metin algilama algoritmasi
  - **default**: Varsayilan algilayici (DBNet + ResNet34)
  - **ctd**: Comic metin algilayici
  - **craft**: CRAFT algilayici

- **Algilama Boyutu (detection_size)**: Algilama sirasindaki gorsel olcekleme boyutu (varsayilan 2048; buyudukce daha dogru ama yavas)

- **Metin Esigi (text_threshold)**: Metin algilama guven esigi (0-1; yukseldikce daha kati)

- **Sinir Kutusu Olusturma Esigi (box_threshold)**: Metin kutusu olusturma guven esigi (deger dusuk olursa daha fazla metin kutusu algilanir)

- **Unclip Orani (unclip_ratio)**: Metin kutusu genisleme orani (metnin genislemesini kontrol eder)

- **Minimum Algilama Kutusu Alan Orani (min_box_area_ratio)**: Gorsel toplam piksellerine oranli minimum algilama kutusu alani (varsayilan 0.0009 = %0.09)
  - Cok kucuk algilama kutularini filtreler
  - Deger yukseldikce filtreleme katilasir; kucuk metin kutulari kaldirilir
  - Deger dusunce daha fazla kucuk metin kutusu korunur
  - Onerilen aralik: 0.0005-0.002

- **YOLO Yardimci Algilama (use_yolo_obb)**: YOLO yonlu sinir kutusuyla yardimci algilama kullan (algilama dogrulugunu arttirir)

- **YOLO Guven Esigi (yolo_obb_conf)**: YOLO yardimci algilamanin guven esigi

- **YOLO Kesisim Orani - IoU (yolo_obb_iou)**: YOLO IOU esigi (kutu cakisma derecelendirme kontrolu)

- **YOLO Yardimci Algilama Cakisma Esigi (yolo_obb_overlap_threshold)**: YOLO kutu cakisma esigi (cakisan algilama kutularini kaldir)

### Onarim Ayarlari

- **Onarim Modeli (inpainter)**: Gorsel onarim algoritmasi
  - **lama_large**: Buyuk LaMa onarim modeli (onerilen, en iyi etki)
  - **lama_mpe**: LaMa MPE onarim modeli (hizli)
  - **default**: AOT onaricisi (varsayilan)

- **Onarim Boyutu (inpainting_size)**: Onarim islemindeki gorsel boyutu (yukseldikce daha iyi etki ama yavas)

- **Onarim Hassasiyeti (inpainting_precision)**: Hassasiyet ayari
  - **fp32**: Tek hassasiyet (en dogru, en yavas)
  - **fp16**: Yarim hassasiyet (denge)
  - **bf16**: BFloat16 (onerilen)

- **PyTorch Onarimini Zorla (force_use_torch_inpainting)**: Gorsel onarim icin PyTorch'u zorla kullan
  - Varsayilan olarak CPU modunda ONNX motoru onceliklidir (daha hizli)
  - Bu secenegi isaretlemek PyTorch motorunu zorla kullandirir
  - Kullanim senaryosu: ONNX motorunda sorun oldugunda veya daha yuksek hassasiyet gerektiginde
  - GPU modunda bu secenek gecersizdir (her zaman PyTorch kullanilir)

### Olusturucu Ayarlari

- **Olusturucu (renderer)**: Olusturma motoru
  - **default**: Varsayilan olusturucu
  - **manga2eng_pillow**: Manga2Eng Pillow olusturucusu

- **Dizim Modu (layout_mode)**: Metin dizim modu
  - **smart_scaling**: Akilli olcekleme (onerilen; yazi tipi boyutunu otomatik ayarlar)
  - **strict**: Kati sinir (metni metin kutusuna sigdirmak icin yazi tipini kucultur)
  - **balloon_fill**: Akilli balon (balonu otomatik algilar ve doldurur)

- **Hizalama (alignment)**: Metin hizalama
  - **auto**: Otomatik hizalama
  - **left**: Sola hizali
  - **center**: Ortaya hizali (yatay ve dikey)
  - **right**: Saga hizali

- **Metin Yonu (direction)**: Yazi yonu
  - **auto**: Otomatik algilama
  - **horizontal**: Yatay dizer
  - **vertical**: Dikey dizer

- **Yazi Tipi Yolu (font_path)**: Yazi tipi dosya yolu (ozel yazi tipi sec)
  - `fonts` dizinine yeni yazi tipi eklenebilir (`.ttf`, `.otf`, `.ttc`)
  - Program acilir menu her acilisinda `fonts` dizinini otomatik tarar
  - Yeni yazi tipi eklendikten sonra yeniden baslatmaya gerek yok

- **Yazi Tipi Sinirini Devre Disi Birak (disable_font_border)**: Yazi tipi sinirini devre disi birak (kontur etkisini kaldir)

- **Kontur Genisligi Orani (stroke_width)**: Yazi tipi kontur (sinir) genisligi; yazi tipi boyutuna oranli
  - Varsayilan: 0.07 (%7)
  - Aralik: 0.0-1.0
  - 0 olarak ayarlamak konturu tamamen devre disi birakir
  - Onerilen aralik: 0.05-0.15

- **AI Satir Sonu (disable_auto_wrap)**: Otomatik satir sonunu devre disi birak (AI satir sonu etkinlestirilince otomatik kapatilir)

- **Yazi Tipi Boyut Ofseti (font_size_offset)**: Yazi tipi boyut ofseti (pozitif buyutur, negatif kucultur)

- **Minimum Yazi Tipi Boyutu (font_size_minimum)**: Minimum yazi tipi boyutu

- **Maksimum Yazi Tipi Boyutu (max_font_size)**: Maksimum yazi tipi boyutu

- **Buyuk Harf (uppercase)**: Buyuk harfe donustur

- **Kucuk Harf (lowercase)**: Kucuk harfe donustur

- **Kesmeci Devre Disi (no_hyphenation)**: Kesme isareti satir sonunu devre disi birak

- **Yazi Tipi Rengi (font_color)**: Yazi tipi rengi (onaltilik renk kodu; ornegin #FFFFFF)

- **Satir Araligi (line_spacing)**: Satir araligi carpani; varsayilan 1.0, aralik 0.1-5.0

- **Yazi Tipi Boyutu (font_size)**: Sabit yazi tipi boyutu (otomatik hesaplamayı gecer)

- **Sembolleri Otomatik Dondur (auto_rotate_symbols)**: Sembolleri otomatik dondur (! ? vb.)

- **Dikey Metinde Yatay (auto_rotate_symbols)**: Dikey metindeki yatay islem (dikey metindeki yatay sembolleri dogru gosterir)

- **SAG'dan SOLA (rtl)**: Sagdan sola dizimi etkinlestir

- **Yazi Tipi Olcekleme Orani (font_scale_ratio)**: Yazi tipini butunuyle olcekle

- **Dikey Ortala (center_text_in_bubble)**: Metin blogunu balon cercevesinde dikey ortala

- **AI Satir Sonu Yazıyı Otomatik Buyut (optimize_line_breaks)**: AI satir sonu optimizasyonunu etkinlestir (satir sonlarini azaltmak icin yazi tipini otomatik ayarla)
  - OpenAI/Gemini cevirici gerektirir
  - AI metin satir sonlarini otomatik optimize eder; okunabilirligi arttirir

- **AI Satir Sonu Kontrolu (check_br_and_retry)**: AI satir sonu sonucunu kontrol et ve yeniden dene (satir sonu kalitesini sagla)

- **AI Satir Sonu Altinda Metin Kutusunu Buyutme (strict_smart_scaling)**: Kati akilli olcekleme modu (AI satir sonunda metin kutusunu buyutme; yalnizca yazi tipini kucultur)

- **Sablon Eslestirme Hizalamasini Etkinlestir (enable_template_alignment)**: Dogrudan yapistirma modunu etkinlestir (yalnizca Ceviriyi Degistir modu)
  - Varsayilan: Kapali
  - Islevi: Koordinat eslesmeye gore cevrilmis gorsellerden bolgeyi keser ve orijinal gorsele yapistir
  - Kullanim senaryosu: Cevrilmis gorselin orijinal yazi tipi, stil, sembol, ses efektlerini korumak isteyenler icin

- **Yapistirma Modu Baglanti Mesafe Orani (paste_connect_distance_ratio)**: Yakin maske bolgelerini baglama mesafe orani; varsayilan 0.03 (%3)

- **Yapistirma Modu Maske Genisleme Boyutu (paste_mask_dilation_pixels)**: Yapistirmadan once maske bolgesi genisleme piksel sayisi; varsayilan 10 piksel; 0 genislemeyi devre disi birakir

### Super Cozunurluk Ayarlari

- **Super Cozunurluk Modeli (upscaler)**: Super cozunurluk modeli
  - **waifu2x**: Waifu2x modeli (varsayilan)
  - **realcugan**: Real-CUGAN modeli (onerilen; daha iyi etki)
  - **mangajanai**: MangaJaNai modeli (en iyi etki; ancak en cok kaynak tuketir)
    - Renkli/siyah-beyaz gorseli otomatik algilar; uygun modeli secer
  - Diger super cozunurluk modelleri

- **Super Cozunurluk Katsayisi (upscale_ratio)**: Buyutme katsayisi
  - **Kullanilmasin**: Super cozunurluk uygulanmaz (varsayilan)
  - **2**, **3**, **4**: 2/3/4 kat buyutme

- **Real-CUGAN Modeli (realcugan_model)**: Yalnizca realcugan secildiginde gecerlidir
  - **2x serisi**: 2x-muhafazakar, 2x-gurultu-yok, 2x-gurultu1x/2x/3x, 2x-gurultu3x-Pro
  - **3x serisi**: 3x-muhafazakar, 3x-gurultu-yok, 3x-gurultu3x, 3x-gurultu3x-Pro
  - **4x serisi**: 4x-muhafazakar, 4x-gurultu-yok, 4x-gurultu3x
  - **Pro Surumu**: Daha iyi etki; biraz yavas
  - **Gurultu Azaltma Yogunlugu**: Sayi yukseldikce gurultu azaltma guclu; gurultulu gorsel icin uygundur

- **Bolum Boyutu (tile_size)**: Bolum isleme boyutu (0 = bolme yok)
  - Varsayilan: 0
  - Onerilen aralik: 200-800
  - Islevi: Buyuk gorseli kucuk parcalara boler; VRAM kullanimini azaltir
  - Kucuklastikca VRAM tasarrufu artar; ancak hiz duser

- **Super Cozunurlugu Geri Al (revert_upscaling)**: Ceviri sonrasi orijinal cozunurlige don (gorsel buyumesini onler)

### Renklendirici Ayarlari

- **Renklendirme Modeli (colorizer)**: Renklendirici turu
  - **none**: Renklendirme yok (varsayilan)
  - Diger renklendirme modelleri

- **Renklendirme Boyutu (colorization_size)**: Renklendirme isleme boyutu (yukseldikce daha iyi etki ama yavas)

- **Gurultu Azaltma Yogunlugu (denoise_sigma)**: Gurultu giderme gucu

---

## Secenekler

### OCR Ayarlari

- **OCR Modeli (ocr)**: OCR tanima modeli
  - **48px**: Varsayilan model (onerilen; hiz ve dogruluk dengesi)
  - **48px_ctc**: CTC modeli (daha yuksek tanima dogrulugu)
  - **mocr**: Manga OCR ozel modeli (manga icin optimize edilmis)
  - **paddleocr**: PaddleOCR motoru (cok dil destegi)
  - **paddleocr_vl**: PaddleOCR-VL-For-Manga modeli (en iyi etki; en cok kaynak tuketir)

- **Karma OCR Etkinlestir (use_hybrid_ocr)**: Karma OCR etkinlestir (iki modeli ayni anda kullan; dogrulugu arttirir)

- **Yedek OCR (secondary_ocr)**: Ikinci OCR modeli (karma OCR'da kullanilir)

- **Minimum Metin Uzunlugu (min_text_length)**: Minimum metin uzunlugu (bu degerden kucuk metinleri filtrele)

- **Balon Disi Metni Yoksay (ignore_bubble)**: Balon disi dialog alanlardaki metni akillica filtrele
  - **Islevi**: Balon olmayan alanlardaki yazilari otomatik algilar ve atlar (baslik, ses efekti, arka plan yazisi vb.)
  - **Parametreler**: 0-1 (0 = devre disi)
  - **Yon Esik Etkisi**:
    - **0**: Devre disi; tum metinleri koru
    - **0.01-0.3**: Gevşek filtreleme; yalnizca belirgin balon disi alanlari filtrele
    - **0.3-0.7**: Orta filtreleme; dogruluk dengesi
    - **0.7-1.0**: Kati filtreleme; normal balon yanlis filtreyabilir
  - **Calisma Prensibi**: Metin kutusu kenar 2 piksel alanindaki siyah-beyaz piksel oranini hesaplar
  - **Kullanim Senaryolari**: Manga'da ses efekti, baslik gibi cevrilmesi gerekmeyen cok sayida yazi varsa

- **Balon Maskesiyle Maske Genislemesini Sinirla (limit_mask_dilation_to_bubble_mask)**: Maske genislemesini balon bolgesiyle sinirla
  - Varsayilan: `false`
  - Etkinlestirilince: Son onarim maskesini modelin balon bolgesiyle kisitlar; onarim araliginin balon disina tasmmasini onler

- **Minimum Metin Bolge Olasiligi (prob)**: OCR tanima olasilik esigi (bu degerden dusuk metinler filtrelenir)

- **MOCR Birlestirme Kullan (use_mocr_merge)**: MOCR birlestirme kullan (yanyana metin bolgelerini birlestir)

- **Birlestirme - Mesafe Toleransi (merge_gamma)**: Birlestirme sirasindaki mesafe toleransi

- **Birlestirme - Aykiri Tolerans (merge_sigma)**: Birlestirme sirasindaki aykiri tolerans

- **Birlestirme - Kenar Oran Esigi (merge_edge_ratio_threshold)**: Kenar metin birlestirme kosulunu kontrol eder

- **Model Yardimli Birlestirme (merge_special_require_full_wrap)**: Model etiketi yardimli on birlestirme sureci etkinlestirme
  - **Acik (varsayilan)**: Model yardimli on birlestirme once calistirilir; on birlestirilen kutular sonraki orijinal birlestirmeye katilmaz
  - **Kapali**: On birlestirme uygulanmaz; tum metin kutulari dogrudan orijinal birlestirme algoritmasinda islenir

### Global Parametreler

- **Konvolusyon Cekirdek Boyutu (kernel_size)**: Metin silme konvolusyon cekirdegi boyutu (varsayilan 3)

- **Maske Genisleme Ofseti (mask_dilation_offset)**: Maske genisleme ofseti (varsayilan 70; metin silme bolgesinin genisleme derecesini kontrol eder)

### Filtre Listesi

Program filtre listesi araciligiyla belirli metin bolgelerini (su damgasi, reklam vb.) atlamayı destekler.

- **Dosya Konumu**: `examples/filter_list.txt`
- **Bicim**: Her satira bir filtre kelimesi; buyuk/kucuk harf duyarsiz; `#` ile baslayan satirlar yorum satiridir
- **Calisma Prensibi**: OCR'nin tanidigi metin filtre kelimesini iceriyorsa metin bolgesi tamamen atlanir (cevrilmez, silinmez, olusturulmaz)
- **Otomatik Olusturma**: Program baslayinca bu dosyayi otomatik olusturur (yoksa)

**Ornek**:
```
# Su damasini filtrele
pixiv
twitter
@username

# Reklami filtrele
reklam
tanitim
```

---

## Yol Yapilandirmasi

### Goreli Yol Tabanı

- **Paketlenmis Surum**: `_internal` dizinine gore
- **Gelistirme Surumu**: Proje kok dizinine gore

### Yaygin Yollar

**Ozel Ipucu Yolu** (`dict` dizini):
- **Sistem Ipuclari** (program dahili; otomatik calistirilir):
  - `dict/system_prompt_hq.json` - Yuksek kaliteli ceviri sistem ipucu
  - `dict/system_prompt_line_break.json` - AI satir sonu sistem ipucu
  - `dict/glossary_extraction_prompt.json` - Terim cikarma sistem ipucu
- **Kullanici Ozel Ipuclari** (arayuzde secilir):
  - `dict/prompt_example.json` - Ipucu ornegi
  - Bu dizine ozel `.json` ipucu dosyasi eklenebilir

**Nasil Ozel Ipucu Eklenir**:

> Bu ipucu su 4 cevirici icin gecerlidir: **OpenAI**, **Gemini**, **Yuksek Kaliteli OpenAI**, **Yuksek Kaliteli Gemini**.

> Onemli: Betik surumu kullanan kullanicilar `prompt_example.json` dosyasini **dogrudan degistirmeyin**; guncelleme sirasinda uzerine yazilir! Lutfen yeni dosya olusturun.

1. "Ozel Ipucu" yanindaki "Dizini Ac" dugmesine tiklayin; `dict` dizinini acin
2. Bu dizinde yeni bir `.json` dosyasi olusturun (ornegin `my_prompt.json`)
3. `prompt_example.json` dosyasini acin; icerigi yeni dosyaya kopyalayin
4. Yeni dosyayi duzenleyin; eser karakteri adlari, terim listesi vb. doldurun
5. Arayuze donup "Ozel Ipucu" acilir menusunden yeni olusturulan dosyayi secin

**Ipucu Ornegi** (JSON sabit bir bicim gerektirmez; herhangi bir gecerli JSON yuklenebilir):

```json
{
  "system_prompt": "Cok dilli uzman bir manga cevirmenisiniz. Gorevniz mangadaki metinleri dogal ve akici hedef dile cevirmektir.\n\nKurallar:\n1. Orijinal metnin tonu, tarzi ve duygularini koruyun.\n2. Asagidaki terim listesine katilikla basvurun.\n3. Belirli bir ceviri yoksa en yaygin cevirmeyi kullanin.",
  "glossary": {
    "Person": [
      {
        "original": "Mashiro",
        "translation": "Mashiro"
      }
    ],
    "Location": [],
    "Org": [],
    "Item": [],
    "Skill": [],
    "Creature": []
  }
}
```

**Alan Aciklamalari**:
- `system_prompt`: Sistem ipucu; ceviri tarzini ve kurallarini tanimlar
- `glossary`: Terim listesi; cesitli ozgun isim kategorilerini icerir
  - `Person`: Kisi adlari
  - `Location`: Yer adlari
  - `Org`: Organizasyon adlari
  - `Item`: Nesne adlari
  - `Skill`: Yetenek adlari
  - `Creature`: Varlik adlari
- Her terim `original` (kaynak) ve `translation` (hedef) alanlarini icerir

> Kolay yontem: JSON yazmayi zahmetli buluyorsaniz su bilgileri AI'ya gonderip olusturmasini isteyin:
> - Eserin orijinal adi ve cevrilmis adi
> - Karakterlerin orijinal adi ve cevrilmis adi
> - `prompt_example.json` icerigini referans bicimi olarak ekleyin

**Orijinal Disa Aktarma Sablon Yolu**:
- Varsayilan: `examples/translation_template.json`
- Orijinal disa aktarma bicimini ozellestirir

**Yazi Tipi Yolu**:
- Varsayilan: `fonts` dizini
- Belirli yazi tipi dosyasi yolu belirtilebilir (ornegin `fonts/my_font.ttf`)
- `.ttf` ve `.otf` formatlarini destekler

**Nasil Ozel Yazi Tipi Eklenir**:
1. Yazi tipi dosyasini (`.ttf` veya `.otf`) `fonts` dizinine kopyalayin
2. Yazi tipi dosya adinin Ingilizce olmasi onerilir (ornegin `myfont.ttf`)
3. Programi yeniden baslatin
4. "Olusturucu Ayarlar"daki "Yazi Tipi Yolu" acilir menusunden yeni yazi tipini secin
5. Veya "Yazi Tipi Yolu" giris kutusuna yazi tipi dosya yolunu girin (ornegin `fonts/myfont.ttf`)

**Cikti Klasoru**:
- Varsayilan: Giris dosyasiyla ayni dizin
- Arayuzde ozel cikti yolu belirtilebilir