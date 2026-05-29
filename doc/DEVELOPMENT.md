# Gelistirici Kilavuzu

Bu belge proje yapisini, gelistirme ortami yapilandirmasini ve derleme/paketleme surecini aciklamaktadir.

---

## Onemli Not

Gelistirme komutlarini calistirmadan once proje dizininde sanal ortami etkinlestirin:

```bash
# Windows / Linux / macOS
conda activate manga-env
```

---

## Proje Yapisi

```
manga-translator-ui-package/
|-- desktop_qt_ui/          # PyQt6 masaustu uygulamasi (ana arayuz)
|   |-- main.py            # Uygulama giris noktasi
|   |-- main_window.py     # Ana pencere
|   |-- app_logic.py       # Is mantigi
|   |-- editor/            # Gorsel duzenleyici
|   |-- services/          # Servis katmani
|   `-- widgets/           # UI bilesenleri
|-- manga_translator/       # Cekirdek ceviri motoru
|   |-- translators/       # Cevirici uygulamalari
|   |-- ocr/              # OCR modulu
|   |-- detection/        # Metin algilama
|   |-- inpainting/       # Gorsel onarim
|   `-- rendering/        # Metin olusturma
|-- fonts/                 # Yazi tipi dosyalari
|-- models/                # AI model dosyalari
|-- examples/              # Yapilandirma ornekleri
`-- requirements_*.txt     # Bagimlilik listeleri
```

---

## Ortam Yapilandirmasi

### Sistem Gereksinimleri

- **Python 3.12**
- **Windows 10/11** veya **Linux**
- **Git** (kodu klonlamak icin)

### Bagimliliklari Kurun

**CPU Surumu:**
```bash
pip install -r requirements_cpu.txt
```

**GPU Surumu (CUDA 12.x gerektirir):**
```bash
pip install -r requirements_gpu.txt
```

---

## Gelistirme Suruimunu Calistirma

### PyQt6 Arayuzunu Calistirin

```bash
python -m desktop_qt_ui.main
```

### Eski CustomTkinter Arayuzunu Calistirin

```bash
python -m desktop-ui.main
```

---

## Derleme ve Paketleme

### PyInstaller Kurun

```bash
pip install pyinstaller
```

### Derleme Betigi Konumu

Derleme betikleri `packaging/` dizinindedir:
- `packaging/build_packages.py` - Derleme betigi
- `packaging/manga-translator-cpu.spec` - CPU surumu yapilandirmasi
- `packaging/manga-translator-gpu.spec` - GPU surumu yapilandirmasi

### CPU Surumunu Derleyin

```bash
cd packaging
python build_packages.py <surum> --build cpu
```

### GPU Surumunu Derleyin

```bash
cd packaging
python build_packages.py <surum> --build gpu
```

### Ornek: 1.6.0 Surumunu Derle

```bash
cd packaging
python build_packages.py 1.6.0 --build cpu
```

---

## Gelistirme Is Akisi

### 1. Depoyu Klonlayin

```bash
git clone https://github.com/turanbagtur/manga-translator-ui.git
cd manga-translator-ui
```

### 2. Sanal Ortam Olusturun

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Bagimliliklari Kurun

```bash
pip install -r requirements_cpu.txt
```

veya

```bash
pip install -r requirements_gpu.txt
```

### 4. Gelistirme Surumunu Calistirin

```bash
python -m desktop_qt_ui.main
```

---

## Hata Ayiklama Ipuclari

### Ayrintili Gunlugu Etkinlestirin

"Temel Ayarlar"da "Ayrintili Gunluk" secenegini isaretleyin; ayrintili isleme surecini goruntuleyin.

### Ara Sonuclari Goruntulemek

Ayrintili gunluk etkinlestirilince program su dosyalari uretir:
- Algilama sonuclari
- OCR tanima sonuclari
- Maske olusturma sureci
- Onarim etkisi

Ayrintilar icin [Hata Ayiklama Kilavuzu](DEBUGGING.md) belgesine bakin.

---

## Kod Standartlari

### Python Kod Stili

- PEP 8 standardina uyun
- 4 bosluk girintileme kullanin
- Fonksiyon ve degiskenler icin snake_case kullanin
- Sinif adlari icin PascalCase kullanin

### Commit Standartlari

- Acik commit mesaji kullanin
- Bir commit'te yalnizca bir sey yapin
- Commit oncesi kodu test edin

---

## Ilgili Kaynaklar

### Cekirdek Motor

- [manga-image-translator](https://github.com/zyddnys/manga-image-translator) - Cekirdek ceviri motoru

### Bagimlilik Kutuphaneleri

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI cercevesi
- [Pillow](https://pillow.readthedocs.io/) - Gorsel isleme
- [PyTorch](https://pytorch.org/) - Derin ogrenme cercevesi
- [OpenCV](https://opencv.org/) - Bilgisayarli goru kutuphanesi

---

## Lisans

Bu proje **GPL-3.0** lisansi altinda acik kaynak kodludur.

Cekirdek ceviri motoru [zyddnys/manga-image-translator](https://github.com/zyddnys/manga-image-translator) projesinden gelmektedir.

---

## Tesekkurler

- [zyddnys/manga-image-translator](https://github.com/zyddnys/manga-image-translator) - Cekirdek ceviri motoru
- Tum katkicilarin ve kullanicilarin destegi