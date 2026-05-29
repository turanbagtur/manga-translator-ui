# Kurulum Kilavuzu

Bu belge ayrintili kurulum adimlarini ve sistem gereksinimlerini aciklamaktadir.

---

## Icindekiler

- [Sistem Gereksinimleri](#sistem-gereksinimleri)
- [Kurulum Yontemi 1: Kurulum Betigi (Onerilen)](#kurulum-yontemi-1-kurulum-betigi-onerilen)
- [Kurulum Yontemi 2: Paketlenmis Surumu Indir](#kurulum-yontemi-2-paketlenmis-surumu-indir)
- [Kurulum Yontemi 3: Kaynak Koddan Calistir](#kurulum-yontemi-3-kaynak-koddan-calistir)
- [Kurulum Yontemi 4: Docker ile Dagitim](#kurulum-yontemi-4-docker-ile-dagitim)
- [Kurulum Yontemi 5: macOS Yerel Calistirma (Apple Silicon)](#kurulum-yontemi-5-macos-yerel-calistirma-apple-silicon)
- [Sorun Giderme](#sorun-giderme)

---

## Sistem Gereksinimleri

### Minimum Gereksinimler

- **Isletim Sistemi**: Windows 10/11 (64-bit), Linux veya macOS 12+ (Apple Silicon)
- **Bellek**: 8 GB RAM
- **Depolama Alani**: 5 GB bos alan (program ve model dosyalari icin)
- **Python Surumu** (gelistirici surumu icin): Python 3.12

### Onerilen Gereksinimler

- **Bellek**: 16 GB RAM veya daha fazla
- **GPU**:
  - **NVIDIA Ekran Karti**: CUDA 12.x destekli (surucu >= 525.60.13 gerektirir)
    - Onerilen VRAM: 6 GB veya daha fazla
    - Desteklenen NVIDIA kartlar: GTX 1060 ve uzeri
  - **AMD Ekran Karti**: ROCm destekli (deneysel)
    - Desteklenen kartlar: **Yalnizca RX 7000/9000 serisi (RDNA 3/4)**
    - RX 5000/6000 serisi icin CPU surumunu kullanin
    - AMD GPU yalnizca kurulum betigi yontemini destekler, paketlenmis surumu desteklemez
    - Windows'ta ROCm destegi sinirlidir, Linux'ta daha iyi calisir
- **Depolama Alani**: 10 GB SSD

---

## Kurulum Yontemi 1: Kurulum Betigi (Onerilen, Miniconda otomatik kurulur)

Betik tum yapilandirmayi otomatik tamamlar ve tek tikla guncellemeyi destekler.

> Ag Notu: Indirme islemi sirasinda GitHub'dan kod cekilir; yavaş ag baglantisi durumunda proxy kullanimi onerilir.
> Yeni Ozellik: Python onceden kurulu olmak zorunda degil; betik Miniconda'yi otomatik kurar (hafif Python ortam yoneticisi).

### On Kosullar

- **Python onceden kurulmak zorunda degil**: Betik Miniconda'yi otomatik indirir ve kurar
- **Git** (istege bagli): Betik tasinalir Git surumunu otomatik indirebilir

### Ayrintili Adimlar

#### 1. Kurulum Betigini Edinin

- Depoya gidin: [https://github.com/turanbagtur/manga-translator-ui](https://github.com/turanbagtur/manga-translator-ui)
- `Adim1-IlkKurulum.bat` dosyasini indirin
- Programi kurmak istediginiz dizine kaydedin (ornegin `D:\manga-translator-ui\`)

#### 2. Kurulum Betigini Calistirin

`Adim1-IlkKurulum.bat` dosyasina cift tiklayin; betik sunlari yapar:

**2.1 Miniconda Algilama ve Kurma**
- Sistemde Python/Conda varsa dogrudan kullanir
- Yoksa:
  - Indirme kaynagi secimi sunar: Tsinghua Universitesi aynasi (yurt ici icin onerilen) veya Anaconda resmi
  - Miniconda3 kurulum programini otomatik indirir (yaklasik 50 MB)
  - `<proje dizini>\Miniconda3` konumuna sessizce kurar (C: surucusunu doldurmaz)
  - Ortam degiskenlerini otomatik yapilandirir
  - **Not**: Kurulum tamamlandiktan sonra betigi yeniden calistirmaniz gerekir (ortam degiskenlerinin yeniden yuklenmesi icin)

**2.2 Git Algilama/Kurma**
- Sistemde Git varsa sistem Git'ini kullanir
- Yoksa iki secenek sunar:
  - **Secenek 1** (onerilen): Tasinalir Git'i otomatik indirir (yaklasik 50 MB)
  - **Secenek 2**: Manuel Git kurduktan sonra yeniden calistirin

**2.3 Indirme Kaynagi Secimi**
- **Secenek 1**: GitHub resmi kaynagi (yurt disi ag icin)
- **Secenek 2** (onerilen): gh-proxy.com aynasi (yurt ici icin daha hizli)

**2.4 Kodu Klonlama/Guncelleme**
- Ilk kurulumda: GitHub'dan kodu klonlar
- Kod zaten varsa: En son suruме otomatik gunceller

**2.5 Conda Ortami Olusturma**
- Proje dizininde `conda_env` ortami olusturur (Python 3.12)
- Konum: `<proje dizini>\conda_env\`
- **C: surucusu sistem alanini kullanmaz**, ortam proje dizinindedir
- Proje bagimliliklar izole edilir, sistem etkilenmez

**2.6 Bagimliliklari Kurma**
- GPU'yu otomatik algilar:
  - **NVIDIA**: CUDA surumusunu algilar; CUDA >= 12 ise GPU surum bagimliliklar kurar (requirements_gpu.txt)
  - **AMD**: Kart modelini ve gfx surumusunu otomatik algilar; kullanici onayindan sonra AMD ROCm PyTorch kurar (requirements_amd.txt); **yalnizca RX 7000/9000 (RDNA 3/4) serisi desteklenir**
  - **Diger/Entegre**: CPU surum bagimliliklar kurar (requirements_cpu.txt)
- Gerekli tum paketleri `launch.py` ile akillica kurar

**2.7 Kurulumu Tamamlama**
- Kurulum konumunu gosterir
- Programi hemen calistirmak isteyip istemediginizi sorar

### Miniconda Ozellikleri

**Avantajlar:**
- Kucuk boyut (yaklasik 50 MB)
- Birden fazla Python surumuyle calisir
- Ortam izolasyonu, birbirini etkilemez
- Dahili pip paket yoneticisi
- **Tamamen proje dizinine kurulur, C: surucusu sistem alanini kullanmaz**

**Dizin Yapisi:**
```
D:\manga-translator-ui\          # Sectiginiz kurulum dizini
|-- Adim1-IlkKurulum.bat         # Kurulum betigi
|-- Adim2-QtArayuzuBaslat.bat    # Baslama betigi
|-- Adim3-GuncellemeKontrolVeBaslat.bat   # Guncelle ve basla
|-- Adim4-GuncellemeVeBakim.bat  # Bakim araci
|-- Miniconda3\                  # Miniconda ana programi (yaklasik 600 MB)
|   |-- python.exe
|   |-- Scripts\
|   |-- pkgs\
|   `-- ...
|-- conda_env\                   # Proje sanal ortami (yaklasik 2-5 GB)
|   |-- python.exe
|   |-- Scripts\
|   |-- Lib\
|   `-- ...
|-- PortableGit\                 # Tasinalir Git (indirilmisse)
|-- desktop_qt_ui\               # Qt arayuzu kaynak kodu
|-- manga_translator\            # Cekirdek ceviri modulu
`-- ...                          # Diger proje dosyalari
```

#### 3. Programi Baslatin

Kurulum tamamlandiktan sonra her seferinde yalnizca sunlari yapmaniz yeterlidir:

`Adim2-QtArayuzuBaslat.bat` dosyasina cift tiklayin

> **Ipucu**: Baslatmadan once guncelleme kontrolu yapmak icin `Adim3-GuncellemeKontrolVeBaslat.bat` dosyasina da cift tiklayabilirsiniz

#### 4. Programi Guncelleme (Istege Bagli)

En son suruме guncellemek istediginizde:

`Adim4-GuncellemeVeBakim.bat` dosyasina cift tiklayin ve "Tam Guncelleme" secenegini secin

---

## Kurulum Yontemi 2: Paketlenmis Surumu Indir

Python kurmak istemeyen kullanicilar icin uygundur; ancak dosya buyuktür (yaklasik 3-5 GB).

### 1. Surumler Sayfasini Ziyaret Edin

[GitHub Releases](https://github.com/turanbagtur/manga-translator-ui/releases) sayfasina gidin.

### 2. Surum Secin

En son surum kurulum paketini indirin:

**CPU Surumu**:
- Dosya adi: `manga-translator-cpu-vX.X.X.zip` veya bolumlu dosya
- Uygulanabilir: Tum bilgisayarlar
- Avantaj: GPU gerekmez, uyumluluk iyi
- Dezavantaj: Ceviri hizi daha yavas

**GPU Surumu**:
- Dosya adi: `manga-translator-gpu-vX.X.X.zip` veya bolumlu dosya
- Uygulanabilir: NVIDIA ekran kartli bilgisayarlar
- Gereksinim: CUDA 12.x destegi
- Avantaj: Ceviri hizi hizli
- Dezavantaj: Uyumlu NVIDIA ekran karti gerektirir

### 3. Bolumlu Indirme Talimatlari

Dosya birden fazla arsivde bolunmussа (ornegin `part1.rar`, `part2.rar`, `part3.rar`...):

1. **Tum bolum dosyalarini indirin**:
   - Tum bolum dosyalarini ayni klasore indirmelisiniz
   - Ornegin: `part1.rar`, `part2.rar`, `part3.rar`

2. **Ilk bolumu acin**:
   - Yalnizca `part1.rar` dosyasina sag tiklayin
   - "Buraya cikart..." veya "Extract to..." secenegini secin
   - Diger bolumler otomatik olarak acma islemine katilir

3. **Onemli Notlar**:
   - Tum bolumler ayni dizinde olmalidir
   - Bolum dosyalarini yeniden adlandirmayin
   - Herhangi bir bolum eksikse acma islemi basarisiz olur

### 4. Kurulum Adimlari

1. **Dosyalari acin**:
   ```
   Indirilen arsivi istediginiz bir dizine cikarin
   Ornegin: D:\manga-translator\
   ```

2. **Dosya yapisini kontrol edin**:
   ```
   manga-translator/
   |-- app.exe          # Ana program
   |-- _internal/       # Bagimlilik dosyalari
   |-- fonts/           # Yazi tipi dosyalari
   |-- models/          # AI model dosyalari
   `-- examples/        # Yapilandirma ornekleri
   ```

3. **Programi calistirin**:
   - `app.exe` dosyasina cift tiklayin
   - Ilk calistirmada model dosyalari otomatik yuklenir

---

## Kurulum Yontemi 3: Kaynak Koddan Calistirma

Gelisitiriciler veya ozellestirme yapmak isteyen kullanicilar icin uygundur.

### 1. Depoyu Klonlayin

```bash
git clone https://github.com/turanbagtur/manga-translator-ui.git
cd manga-translator-ui
```

### 2. Bagimliliklari Kurun

```bash
# CPU surumu
pip install -r requirements_cpu.txt

# GPU surumu (CUDA 12.x gerektirir)
pip install -r requirements_gpu.txt
```

### 3. Programi Calistirin

```bash
# PyQt6 arayuzunu calistirin
python -m desktop_qt_ui.main
```

---

## Kurulum Yontemi 4: Docker Imaji ile Dagitim (Deneysel)

BT paneli, Portainer gibi Docker yonetim araclari kullanan kullanicilar icin uygundur.

### Hizli Baslangic

**Windows CMD / PowerShell**:
```cmd
docker run -d --name manga-translator -p 8000:8000 hgmzhn/manga-translator:latest-cpu
```

**Linux / macOS**:
```bash
docker run -d --name manga-translator -p 8000:8000 hgmzhn/manga-translator:latest-cpu
```

Baslatildiktan sonra erisim:
- Kullanici Arayuzu: http://localhost:8000
- Yonetim Arayuzu: http://localhost:8000/admin.html

### Imaj Deposu

Bu projenin Docker imajlari iki ayri depoda yayimlanmaktadir; daha hizli olani secin:

**Docker Hub (Onerilen)**:
- CPU Surumu: `hgmzhn/manga-translator:latest-cpu`
- GPU Surumu: `hgmzhn/manga-translator:latest-gpu`

**GitHub Container Registry (Yedek)**:
- CPU Surumu: `ghcr.io/hgmzhn/manga-translator:latest-cpu`
- GPU Surumu: `ghcr.io/hgmzhn/manga-translator:latest-gpu`

> Her iki depodaki imajlar aynidir; daha hizli olanı secin.

### Port Eslemesi

- **Konteyner Portu**: `8000`
- **Ana Makine Portu**: `8000` (ozellestirilebilir)

### Ortam Degiskeni Yapilandirmasi

> Tum ortam degiskenleri istege baglidir; program makul varsayilan degerleri kullanir.

#### Temel Yapilandirma (Istege Bagli)

| Degisken | Ornek | Varsayilan | Aciklama |
|----------|-------|------------|----------|
| `MT_WEB_HOST` | `0.0.0.0` | `0.0.0.0` | Dinleme adresi (0.0.0.0 dis erisime izin verir, 127.0.0.1 yalnizca yerel erisim) |
| `MT_WEB_PORT` | `8000` | `8000` | Servis portu |
| `MT_USE_GPU` | `true` | `false` | GPU kullanimi (yalnizca GPU surumu imajinda ayarlanmalidir) |
| `MT_MODELS_TTL` | `300` | `0` | Modelin bellekte yasam suresi (saniye), 0 = kalici |
| `MT_RETRY_ATTEMPTS` | `-1` | `None` | Ceviri hatasi yeniden deneme sayisi, -1 = sinirsiz |
| `MT_VERBOSE` | `true` | `false` | Ayrintili gunluk gosterimi |
| `MANGA_TRANSLATOR_ADMIN_PASSWORD` | `your_password` | Yok | Yonetici sifresi (en az 6 karakter; ayarlanmazsa yonetim arayuzune erisemezsiniz) |

#### API Key Yapilandirmasi (Kullandiginiz ceviriciye gore secin)

**OpenAI Serisi**:
| Degisken | Aciklama |
|----------|----------|
| `OPENAI_API_KEY` | OpenAI API Key (openai, openai_hq ceviricileri icin) |
| `OPENAI_MODEL` | OpenAI model adi (istege bagli, varsayilan gpt-4o) |
| `OPENAI_API_BASE` | OpenAI API taban URL (istege bagli, varsayilan resmi adres) |
| `OPENAI_HTTP_PROXY` | OpenAI HTTP proxy (istege bagli) |
| `OPENAI_GLOSSARY_PATH` | OpenAI sozluk yolu (istege bagli, varsayilan ./dict/mit_glossary.txt) |

**Google Gemini Serisi**:
| Degisken | Aciklama |
|----------|----------|
| `GEMINI_API_KEY` | Google Gemini API Key (gemini, gemini_hq ceviricileri icin) |
| `GEMINI_MODEL` | Gemini model adi (istege bagli, varsayilan gemini-1.5-flash-002) |
| `GEMINI_API_BASE` | Gemini API taban URL (istege bagli) |

**Diger Ticari Ceviri Servisleri**:
| Degisken | Aciklama |
|----------|----------|
| `DEEPL_AUTH_KEY` | DeepL API Key |
| `GROQ_API_KEY` | Groq API Key |
| `GROQ_MODEL` | Groq model adi (istege bagli, varsayilan mixtral-8x7b-32768) |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |
| `DEEPSEEK_API_BASE` | DeepSeek API taban URL (istege bagli) |
| `DEEPSEEK_MODEL` | DeepSeek model adi (istege bagli, varsayilan deepseek-chat) |
| `TOGETHER_API_KEY` | Together AI API Key |
| `TOGETHER_VL_MODEL` | Together AI gorseli modeli (istege bagli) |

**Yerel/Ozel Modeller**:
| Degisken | Aciklama |
|----------|----------|
| `SAKURA_API_BASE` | Sakura API adresi (varsayilan http://127.0.0.1:8080/v1) |
| `SAKURA_VERSION` | Sakura API surumu (istege bagli, 0.9 veya 0.10) |
| `SAKURA_DICT_PATH` | Sakura sozluk yolu (istege bagli) |
| `CUSTOM_OPENAI_API_KEY` | Ozel OpenAI uyumlu API Key (varsayilan ollama) |
| `CUSTOM_OPENAI_API_BASE` | Ozel OpenAI uyumlu API adresi (varsayilan http://localhost:11434/v1) |
| `CUSTOM_OPENAI_MODEL` | Ozel model adi (ornegin qwen2.5:7b) |
| `CUSTOM_OPENAI_MODEL_CONF` | Ozel model yapilandirmasi (ornegin qwen2) |

> Yalnizca kullanmak istediginiz ceviriciye karsilik gelen API Key'i yapilandirmaniz yeterlidir.

### Erisim Adresi

Dagitim basarili olduktan sonra:
- **Kullanici Arayuzu**: `http://sunucu-IP:8000`
- **Yonetim Arayuzu**: `http://sunucu-IP:8000/admin.html` (yonetici sifresi gerektirir)

### BT Paneli Dagitim Adimlari

1. **Portu acin**: BT Paneli -> Guvenlik -> 8000 portuna izin verin
2. **Docker kurun**: Yazilim Magazasi -> Docker Yoneticisi -> Kur
3. **Imaj cekin**: Docker Yoneticisi -> Imajlar -> Depodan cek
4. **Konteyner olusturun**: Konteyner -> Konteyner Olustur -> Port eslemesi `8000:8000`
5. **Konteyneri baslatip** `http://sunucu-IP:8000` adresine erisim saglayin

> Docker imaj islevi simdilik deneysel asama olup bilinmeyen sorunlar icermektedir.

---

## Kurulum Yontemi 5: macOS Yerel Calistirma (Apple Silicon)

Apple Silicon (M1/M2/M3/M4) islemcili Mac icin tasarlanmistir; MPS (Metal Performance Shaders) yerel GPU hizlandirmasini kullanir.

### Sistem Gereksinimleri

- **Donanim**: Mac bilgisayar (M1/M2/M3/M4; Intel Mac da calisir ancak CPU modunu kullanir)
- **Sistem**: macOS 12.0 veya uzeri
- **Yazilim**: Xcode Komut Satiri Araclari (betik otomatik kontrol eder ve kurulumu ister)

### Betik Aciklamalari

Proje, Windows toplu dosyalarinin karsiliklarini olusturan 4 adet macOS betigi icerir:

| Betik Dosyasi | Aciklama | Windows Karsiligi |
|---------------|----------|-------------------|
| `macOS_1_IlkKurulum.sh` | Ilk ortam yapılandirmasi, kod klonlama, Miniforge kurulumu, bagimlilik kurulumu | Adim1-IlkKurulum.bat |
| `macOS_2_QtArayuzuBaslat.sh` | Grafik arayuzunu baslatir | Adim2-QtArayuzuBaslat.bat |
| `macOS_3_GuncellemeKontrolVeBaslat.sh` | Surum guncelleme kontrolu yapip baslatir | Adim3-GuncellemeKontrolVeBaslat.bat |
| `macOS_4_GuncellemeVeBakim.sh` | Bakim menusunu calistirir (kod guncelleme, bagimlilik guncelleme, onbellek temizleme vb.) | Adim4-GuncellemeVeBakim.bat |

### Kurulum Adimlari

**Yontem 1: Hizli Kurulum (Onerilen)**

Yalnizca kurulum betigini indirin; geri kalanlar otomatik:

```bash
# 1. Kurulum betigini indirin
curl -O https://raw.githubusercontent.com/turanbagtur/manga-translator-ui/main/macOS_1_IlkKurulum.sh

# 2. Calistirma izni verin
chmod +x macOS_1_IlkKurulum.sh

# 3. Kurulumu calistirin
./macOS_1_IlkKurulum.sh
```

Betik otomatik olarak sunlari tamamlar:
- Xcode Komut Satiri Araclari'nin (Git dahil) kurulu olup olmadigini kontrol eder ve kurar
- Proje kodunu klonlar
- Miniforge'u algilar ve kurar (kurulu degilse)
- Bagimsiz `manga-env` sanal ortami olusturur (Python 3.12)
- Tum bagimliliklari kurar (`requirements_metal.txt` kullanarak)
- MPS GPU hizlandiirmasini yapilandirir

**Yontem 2: Manuel Klonlama**

Kodu onceden incelemek veya Git'e sahip olmak isteyenler icin:

```bash
# 1. Depoyu klonlayin
git clone https://github.com/turanbagtur/manga-translator-ui.git
cd manga-translator-ui

# 2. Calistirma izni verin
chmod +x macOS_*.sh

# 3. Kurulumu calistirin
./macOS_1_IlkKurulum.sh
```

### Dogrulama ve Baslangic

Kurulum tamamlandiktan sonra:

- **Normal Baslangic**:
  ```bash
  ./macOS_2_QtArayuzuBaslat.sh
  ```

- **Guncelleme Kontrolu Yapip Baslatma**:
  ```bash
  ./macOS_3_GuncellemeKontrolVeBaslat.sh
  ```

- **Guncelleme ve Bakim**:
  ```bash
  ./macOS_4_GuncellemeVeBakim.sh
  ```
  Bakim menusu sunlari saglar:
  - Kodu guncelle (uzaga zorla senkronize et)
  - Bagimliliklari guncelle/kur
  - Tam guncelleme (kod + bagimliliklar)
  - Onarim modu (tum bagimliliklari yeniden kur)

### Sik Sorulan Sorular

**S: Ilk kurulum ne kadar surer?**
C: Ag hizina bagli olarak yaklasik 10-20 dakika. Yaklasik 2 GB bagimlilik paketi indirilir.

**S: Intel Mac kullanilabilir mi?**
C: Evet; betik otomatik olarak algilar ve Intel surum Miniforge'u kullanir, ancak yalnizca CPU modu kullanilabilir (MPS hizlandirmasi olmadan).

**S: En son suruме nasil guncelleme yapilir?**
C: `./macOS_4_GuncellemeVeBakim.sh` dosyasini calistirip "Tam Guncelleme" secenegini secin.

---

## Ilk Calistirma

### 1. Programi Baslatma

`app.exe` dosyasina cift tiklayin; program otomatik olarak:
- AI modellerini yukler (ilk calistirmada birkaç dakika surer)
- Ceviri motorunu baslatir
- Ana arayuzu acar

### 2. Temel Ayarlar (CPU Surumu Kullanicilari Icin Zorunlu)

**CPU surumu** kullaniyorsaniz mutlaka:

1. "Temel Ayarlar" sekmesine tiklayin
2. **"GPU Kullan" seceneginin isaretini kaldilin**
3. "Yapilandirmayi Kaydet" dugmesine tiklayin

> CPU surumunda GPU etkinlestirmek programa cokmasina neden olur!

### 3. Cikti Dizinini Ayarlama

1. Ana arayuzde "Cikti Klasoru Sec" dugmesine tiklayin
2. Ceviri sonuclarinin kaydedilecegi konumu secin
3. Program bu ayari hatirlar

### 4. Cevirici Secme

1. "Temel Ayarlar" bolumunde "Cevirici" acilir menusunu bulun
2. Ilk kullanim icin onerilen:
   - **Yuksek Kaliteli OpenAI** veya **Yuksek Kaliteli Gemini** (cok modlu, gorsel ceviri, en iyi sonuc) - Kesinlikle Onerilen
   - API Key yapilandirmasi gerekir -> [API Yapilandirma Kilavuzu](API_CONFIG.md)

### 5. Gorsel Ekleme

Gorsel eklemek icin desteklenen yontemler:

- **Yontem 1**: "Dosya Ekle" dugmesine tiklayin
- **Yontem 2**: "Klasor Ekle" dugmesine tiklayin
- **Yontem 3**: Gorselleri dogrudan pencereye surukleyin

Desteklenen gorsel formatlari: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`

### 6. Ceviriyi Baslatin

1. Ayarlarinizi dogrulayin
2. "Ceviriyi Basla" dugmesine tiklayin
3. Ceviri tamamlanmasini bekleyin
4. Sonuclar otomatik olarak cikti klasorune kaydedilir

---

## Sorun Giderme

### Program Baslamiyor

**Sorun**: `app.exe` dosyasina cift tiklayinca tepki yok veya aninda kapaniyor

**Cozum**:
1. Tum dosyalarin acilip acilmadigini kontrol edin (arsiv icinden dogrudan calistirmayin)
2. Antivirusun programi engelleyip engellemedigini kontrol edin
3. `app.exe` dosyasini yonetici olarak calistirin
4. `logs/error.log` dosyasina bakin

### DLL Dosyasi Eksik

**Sorun**: `VCRUNTIME140.dll` veya baska DLL dosyasi eksik uyarisi

**Cozum**:
1. [Microsoft Visual C++ Yeniden Dagitilab](https://aka.ms/vs/17/release/vc_redist.x64.exe) indirip kurun
2. Bilgisayari yeniden baslatın
3. Programi yeniden calistirin

### GPU Surumu Cokuyor

**Sorun**: GPU surumu calisirken cokuyor veya hata veriyor

**Cozum**:
1. Ekran kartinin CUDA 12.x destekleyip desteklemedigini dogrulayin
2. NVIDIA ekran karti surucusunu kurun veya guncelleyin
3. [CUDA Toolkit 12.x](https://developer.nvidia.com/cuda-downloads) indirip kurun
4. Hala basarisizsa CPU surumunu kullanin

### Ceviri Basarisiz

**Sorun**: Gorsel eklendiginde ceviri basarisiz oluyor

**Cozum**:
1. Gorsel formatinin desteklenip desteklenmedigini kontrol edin
2. `models/` dizinindeki model dosyalarinin tam oldugunu dogrulayin
3. "Temel Ayarlar"da "Ayrintili Gunluk" secenegini isaretleyerek hata bilgilerini goruntuleyin
4. `logs/app.log` dosyasina bakin

### Model Yukleme Yavas

**Sorun**: Ilk calistirmada model yukleme suresi cok uzun

**Neden**: Program birden fazla AI model dosyasi yuklemesi gerekiyor (toplam yaklasik 2-3 GB)

**Oneriler**:
- Ilk calistirmada 5-10 dakika sabırla bekleyin
- Sonraki calistirmalar cok daha hizli olur (modeller onbellege alinmistir)
- Yukleme hizini artirmak icin SSD'ye kurulum onerilir

---

## Sonraki Adimlar

Kurulum tamamlandiktan sonra su belgeleri okumanizi oneririz:

- [Ozellikler](FEATURES.md) - Programin tum ozelliklerini ogrenin
- [Is Akislari](WORKFLOWS.md) - Farkli ceviri is akislarini ogrenin
- [Ayarlar](SETTINGS.md) - Cevirici ve parametreleri yapilandirin

---

[Ana Sayfa](../README.md)'ya don