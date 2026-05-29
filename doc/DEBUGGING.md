# Hata Ayiklama Kilavuzu

Bu belge ceviri sonuclarinin hata ayiklamasini ve sorunlarin giderilmesini aciklamaktadir.

---

## Hata Ayiklama Sureci

Ceviri sonuclari istenilen gibi degilse ayrintili gunluk ile ara isleme adimlarini goruntuleyerek sorunun kaynagini bulabilirsiniz.

---

## Ayrintili Gunlugu Etkinlestirin

"Temel Ayarlar" sekmesinde **Ayrintili Gunluk** secenegini isaretleyin.

---

## Hata Ayiklama Dosyasi Aciklamasi

Ayrintili gunluk etkinlestirildikten sonra her calistirmada `result/zaman-damgasi-gorsel-adi-hedef-dil-cevirici/` klasorunde hata ayiklama dosyalari olusturulur:

### Algilama Asamasi

- **`detection_raw_boxes.png`**: Algilayicinin cikarttigi ham metin kutulari (filtrelenmemis)
  - Algilayicinin buldugu tum olasi metin bolgelerini gosterir
  - Her kutu farkli renkle isaretlenir

- **`bboxes_unfiltered.png`**: Algilayici filtrelemesinden gecmis metin kutulari (OCR filtrelemesi uygulanmamis)
  - Algilayici guven esigini gecen metin kutularini gosterir
  - Kirmizi cerceve ile isaretlenir

- **`hybrid_detection_boxes.png`**: Karma algilama sonuclari (birden fazla algilayici etkinse)
  - Birden fazla algilayicinin sonuclarinin birlesimini gosterir

### OCR Asamasi

- **`ocrs/` klasoru**: Her metin kutusunun OCR tanima gorseli
  - `0.png`, `1.png`, `2.png`... her dosya bir metin kutusuna karsilik gelir
  - OCR'nin tanimladigi belirli icerikleri goruntuleyin
  - Dikey metin otomatik olarak yatay goruntuleme icin donduruluir

- **`bboxes.png`**: OCR filtrelemesinden gecmis son metin kutulari
  - Metnin basariyla tanindigi metin kutularini gosterir
  - Metin olasiligi guven bilgisi icerir
  - Metin kutularinin okuma sirasi (panel numarasi) gosterilir

### Maske ve Onarim Asamasi

- **`bboxes_with_scores.png`**: Guven puanli metin kutulari
  - Her metin kutusunun algilama guvenini gosterir

- **`mask_binary.png`**: Ikilestirme maskesi
  - Metin bolgelerinin siyah-beyaz maskesi

- **`mask_raw.png`**: Ham metin silme maskesi (isi haritasi)
  - Optimize edilmemis ham maske; guven duzeyini gosteren renk cubugu ile birlikte

- **`mask_comparison.png`**: Maske karsilastirma gorseli (birden fazla maske varsa)
  - Farkli maske olusturma yontemlerinin etkisini karsilastirir

- **`mask_final.png`**: Optimize edilmis metin silme maskesi
  - Genisleme ve optimizasyondan gecmis son maske

- **`inpaint_input.png`**: Onarim modeline giren gorsel
  - Onarlmak uzere hazirlanan gorsel

- **`inpainted.png`**: Metin silinmis gorsel
  - Metin silme ve arka plan onariminin sonucu

### Olusturma Asamasi

- **`balloon_fill_boxes.png`**: Akilli balon modundaki metin kutulari (balloon_fill dizimi kullaniliyorsa)
  - Akilli balon dizimindeki metin kutusu konumlarini gosterir

- **`final.png`**: Son ceviri sonucu
  - Ceviri metni olusturulmus tam gorsel

### Diger Hata Ayiklama Dosyalari

- **`input.png`**: Orijinal giris gorseli (bazi isleme modlarinda)
  - Kaydedilen orijinal giris gorseli

---

## Ayarlanabilir Parametreler

Algilama veya tanima sonuclari istenilen gibi degilse "Gelismis Ayarlar" sekmesinde asagidaki parametreleri ayarlayin:

### Algilayici Parametreleri

- **Metin Guven Degeri** (text_threshold): `0.1 - 0.9`, varsayilan `0.5`
  - Algilayicinin bir bolgeyi metin olarak nitelendirme guven esigi
  - **Dusurun**: Daha fazla metin algilar; ancak metin olmayan bolgeleri yanlis algilayabilir
  - **Artirin**: Yalnizca belirgin metni algilar; bulanik metni kacirebilir

- **Metin Kutusu Olusturma Guven Degeri** (box_threshold): `0.1 - 0.9`, varsayilan `0.5`
  - Metin kutusu olusturmak icin guven esigi
  - **Dusurun**: Daha fazla metin kutusu olusturur
  - **Artirin**: Yalnizca yuksek guvenli metin kutulari olusturur

- **Unclip Orani** (unclip_ratio): `1.0 - 3.0`, varsayilan `2.5`
  - Metin kutusu genisleme orani
  - **Artirin**: Metin kutusu daha buyur; cevresindeki bolgeyi daha fazla icerir
  - **Dusurun**: Metin kutusu daha kompakt; metne yakin

### OCR Parametreleri

- **OCR Guven Degeri** (prob): `0.0 - 1.0`, varsayilan `0.1`
  - OCR tanima metninin guven esigi
  - **Dusurun**: Daha fazla tanima sonucu korur; ancak yanlis tanıma icerebilir
  - **Artirin**: Yalnizca yuksek guvenli tanima sonuclarini korur; bazi metinleri kacirebilir

---

## Hata Ayiklama Sureci Ornegi

1. **Algilama Asamasini Kontrol Edin**:
   - `bboxes_unfiltered.png` dosyasina bakin; algilayicinin tum metin bolgelerini bulup bulmadigini dogrulayin
   - Eksik algilama varsa: **Metin Guven Degeri** ve **Metin Kutusu Olusturma Guven Degeri**'ni dusurun
   - Yanlis algilama varsa: **Metin Guven Degeri** ve **Metin Kutusu Olusturma Guven Degeri**'ni artirin

2. **OCR Asamasini Kontrol Edin**:
   - `ocrs/` klasoründeki gorsellere bakin; her metin kutusunun icerigi dogrulayin
   - `bboxes.png` dosyasina bakin; hangi metin kutularinin basariyla tanindığini dogrulayin
   - Tanıma orani dusukse: **OCR Guven Degeri**'ni dusurun veya **Unclip Oranini** artirin (metin kutusunun cevresindeki bolgeyi daha fazla icerecek sekilde)
   - Yanlis tanima fazlaysa: **OCR Guven Degeri**'ni artirin

---

## Sik Sorulan Sorun Giderme

### Metin Algilanmiyor

**Olasi Nedenler**:
- Algilama guven degeri cok yuksek
- Gorsel cozunurlugu cok dusuk
- Metin rengi ile arka plan kontrasti dusuk

**Cozum**:
1. "Metin Guven Degeri" ve "Sinir Kutusu Olusturma Esigini" dusurun
2. "Algilama Boyutunu" artirin (ornegin 2560 veya 3072)
3. Gorsel kalitesini iyilestirip yeniden deneyin ya da "Algilama Boyutunu" artirmaya oncelik verin

### OCR Tanimasi Hatali

**Olasi Nedenler**:
- Metin kutusu cok kucuk veya cok buyuk
- Metin bulanik veya bozuk
- OCR modeli uygun degil

**Cozum**:
1. "Unclip Oranini" ayarlayarak metin kutusunun daha uygun olmasi saglayin
2. Farkli OCR modeli deneyin (48px, 48px_ctc, mocr)
3. Iki modeli ayni anda kullanan "Karma OCR"yi etkinlestirin

### Ceviri Sonucu Dizimi Hatali

**Olasi Nedenler**:
- Yazi tipi boyutu uygun degil
- Dizim modu uygun degil
- Metin kutusu konumu dogru degil

**Cozum**:
1. "Dizim Modu"nu ayarlayin (onerilen: "Akilli Olcekleme")
2. "Yazi Tipi Boyut Ofseti"ni degistirin
3. Gorsel duzenleyicide metin kutularini elle ayarlayin

### Metin Silme Temiz Degil

**Olasi Nedenler**:
- Maske araligı yeterli degil
- Onarim modelinin etkisi yetersiz

**Cozum**:
1. "Maske Genisleme Ofseti"ni artirin (varsayilan 70; 100-150'ye cikartilabilir)
2. Onarim modelini "lama_large" olarak degistirin (en iyi etki)
3. Gorsel duzenleyicide maskeyi elle duzenleyin