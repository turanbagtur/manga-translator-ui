<div align="center">

<img src="doc/images/ana-sayfa.png" width="500" alt="Ana Sayfa">

[![DeepWiki Belgeleri](https://img.shields.io/badge/DeepWiki-Çevrimiçi_Belgeler-blue)](https://deepwiki.com/hgmzhn/manga-translator-ui)
[![Tabanlı](https://img.shields.io/badge/Tabanlı-manga--image--translator-green)](https://github.com/zyddnys/manga-image-translator)
[![Model](https://img.shields.io/badge/Model-Real--CUGAN-orange)](https://github.com/bilibili/ailab)
[![Model](https://img.shields.io/badge/Model-MangaJaNai-orange)](https://github.com/the-database/MangaJaNai)
[![Model](https://img.shields.io/badge/Model-YSG-orange)](https://github.com/lhj5426/YSG)
[![Model](https://img.shields.io/badge/Model-MangaLens%20Bubble%20Segmentation-orange?logo=huggingface)](https://huggingface.co/huyvux3005/manga109-segmentation-bubble)
[![OCR](https://img.shields.io/badge/OCR-PaddleOCR-blue)](https://github.com/PaddlePaddle/PaddleOCR)
[![OCR](https://img.shields.io/badge/OCR-MangaOCR-blue)](https://github.com/kha-white/manga-ocr)
[![OCR](https://img.shields.io/badge/OCR-PaddleOCR--VL-blue)](https://github.com/jzhang533/PaddleOCR-VL-For-Manga)
[![Lisans](https://img.shields.io/badge/Lisans-GPL--3.0-red)](LICENSE)

</div>


Manga görsellerindeki metinleri tek tıkla çevirin. Japon, Kore ve Amerikan mangalarını destekler; siyah-beyaz ve renkli mangalar tanınabilir. Otomatik algılama, çeviri ve metin yerleştirme; Japonca, Çince, İngilizce ve daha fazla dili destekler. Yerleşik görsel editör ile metin kutularını düzenleyebilirsiniz.

**🐛 [Sorun Bildir](https://github.com/hgmzhn/manga-translator-ui/issues)**

---

## 📚 Belge Rehberi

| Belge | Açıklama |
|-------|----------|
| [Kurulum Kılavuzu](doc/INSTALLATION.md) | Ayrıntılı kurulum adımları, sistem gereksinimleri, bölünmüş indirme talimatları |
| [Kullanım Kılavuzu](doc/USAGE.md) | Temel işlemler, çevirici seçimi, genel ayarlar |
| [Komut Satırı Modu](doc/CLI_USAGE.md) | Komut satırı kullanım kılavuzu, parametre açıklamaları, toplu işleme |
| [API Yapılandırması](doc/API_CONFIG.md) | API Key başvurusu, yapılandırma eğitimi |
| [Özellikler](doc/FEATURES.md) | Tam özellik listesi, görsel editör detayları |
| [İş Akışları](doc/WORKFLOWS.md) | 7 iş akışı, AI satır sonu, özel şablonlar |
| [Ayarlar](doc/SETTINGS.md) | Çevirici yapılandırması, OCR modelleri, parametre detayları |
| [Hata Ayıklama](doc/DEBUGGING.md) | Hata ayıklama süreci, ayarlanabilir parametreler, sorun giderme |
| [Geliştirici Kılavuzu](doc/DEVELOPMENT.md) | Proje yapısı, ortam yapılandırması, derleme ve paketleme |

---

## 📸 Örnek Sonuçlar

<div align="center">

<table>
<tr>
<td align="center"><b>Çeviri Öncesi</b></td>
<td align="center"><b>Çeviri Sonrası</b></td>
</tr>
<tr>
<td><img src="doc/images/0012.png" width="400" alt="Çeviri Öncesi"></td>
<td><img src="doc/images/110012.png" width="400" alt="Çeviri Sonrası"></td>
</tr>
</table>

</div>

---

## ✨ Temel Özellikler

### Çeviri Özellikleri

- 🔍 **Akıllı Metin Algılama** - Mangadaki metin bölgelerini otomatik tanır
- 📝 **Çok Dilli OCR** - Japonca, Çince, İngilizce ve daha fazlasını destekler
- 🌐 **5 Çeviri Motoru** - OpenAI, Gemini (standart + yüksek kalite), Sakura
- 🎯 **Yüksek Kaliteli Çeviri** - GPT-4o, Gemini çok modlu AI çevirisini destekler
- 📚 **Otomatik Terim Çıkarımı** - AI özel isimleri otomatik tanır ve biriktirir, çeviri tutarlılığını sağlar
- 🤖 **AI Akıllı Satır Sonu** - Metin okunabilirliğini artırır, satır sonlarını otomatik optimize eder
- 🎨 **Akıllı Metin Yerleştirme** - Çeviriyi otomatik düzenler, birden fazla yazı tipini destekler
- 📥 **PSD Dışa Aktarma** - Düzenlenebilir PSD dosyaları dışa aktarır (orijinal/onarılmış/metin katmanları)
- 📦 **Toplu İşleme** - Tüm klasörü tek seferde işler

### Görsel Editör

- ✏️ **Alan Düzenleme** - Metin kutularını taşı, döndür, şekillendir
- 📐 **Metin Düzenleme** - Manuel çeviri, stil ayarları
- 🖌️ **Maske Düzenleme** - Fırça aracı, silgi
- ⏪ **Geri Al/Yeniden Yap** - Tam işlem geçmişi
- ⌨️ **Kısayol Tuşları** - A/D ile resim değiştirme, Q/W/E ile araç değiştirme, Ctrl+Q/W/E ile dosya işlemleri
- 🖱️ **Fare Tekerleği Kısayolları** - Ctrl+tekerlek ile metin kutusu boyutlandırma, Shift+tekerlek ile fırça boyutu ayarı

**Tüm Özellikler** → [doc/FEATURES.md](doc/FEATURES.md)

---

## 🚀 Hızlı Başlangıç

### 📥 Kurulum Yöntemleri

#### Yöntem 1: Kurulum Betiği (⭐ Önerilen, güncelleme desteği)

> ⚠️ **Python kurulu olmasına gerek yok**: Betik Miniconda'yı otomatik kurar (hafif Python ortamı)  
> 💡 **Tek tıkla güncelleme**: Kurulu kullanıcılar `Adim4-GuncellemeVeBakim.bat` dosyasını çalıştırarak en son sürüme güncelleyebilir

1. **Kurulum betiğini indirin**:
   - [Adim1-IlkKurulum.bat dosyasını indirmek için tıklayın](https://github.com/hgmzhn/manga-translator-ui/raw/main/Adim1-IlkKurulum.bat)
   - Programı kurmak istediğiniz dizine kaydedin (örn. `D:\manga-translator-ui\`)
   - ⚠️ **Bu dizin kurulumun kök dizini olacak**, tüm program dosyaları buraya kurulur
   - ⚠️ **Temizlik uyarısı**: Temizleme işlevi tüm kök dizin içeriğini siler, ancak Python ve Git yapılandırma dosyalarını korur

2. **Kurulumu çalıştırın**:
   - `Adim1-IlkKurulum.bat` dosyasına çift tıklayın
   - Betik otomatik olarak şunları yapar:
     - ✓ Miniconda'yı algılar ve kurar (gerekirse)
       - İndirme kaynağı seçimi sunar: Tsinghua Üniversitesi aynası (yurt içi için önerilen) veya Anaconda resmi
       - Otomatik indirir ve kurar (yaklaşık 50MB)
       - Proje dizinine kurar, C: sürücüsünü doldurmaz
     - ✓ Taşınabilir Git kurar (gerekirse)
     - ✓ Kod deposunu klonlar
     - ✓ Conda sanal ortamı oluşturur (Python 3.12)
     - ✓ Ekran kartı türünü algılar (NVIDIA / AMD / Entegre)
     - ✓ Uygun PyTorch sürümünü otomatik seçer
       - NVIDIA: CUDA 12.x sürümü (sürücü >= 525.60.13 gerektirir)
       - AMD: ROCm sürümü (deneysel destek, **yalnızca RX 7000/9000 serisi desteklenir**, RX 5000/6000 için CPU sürümünü kullanın)
       - Diğer: CPU sürümü (evrensel, daha yavaş)
     - ✓ Tüm bağımlılıkları kurar

3. **Programı başlatın**:
   - `Adim2-QtArayuzuBaslat.bat` dosyasına çift tıklayın

#### Yöntem 2: Paketlenmiş Sürümü İndir

1. **Programı indirin**:
   - [GitHub Releases](https://github.com/hgmzhn/manga-translator-ui/releases) sayfasına gidin
   - Sürüm seçin:
     - **CPU Sürümü**: Tüm bilgisayarlarda çalışır
     - **GPU Sürümü (NVIDIA)**: CUDA 12.x destekleyen NVIDIA ekran kartı gerektirir
     - ⚠️ **AMD GPU paketlenmiş sürümü desteklemez**, lütfen "Yöntem 1: Kurulum Betiği"ni kullanın

2. **Arşivi açıp çalıştırın**:
   - Arşivi istediğiniz dizine çıkarın
   - `app.exe` dosyasına çift tıklayın

#### Yöntem 3: Docker ile Dağıtım (Deneysel)

**Hızlı Başlatma**:
```bash
# Windows CMD / PowerShell
docker run -d --name manga-translator -p 8000:8000 hgmzhn/manga-translator:latest-cpu

# Linux / macOS
docker run -d --name manga-translator -p 8000:8000 hgmzhn/manga-translator:latest-cpu
```

**İmaj Deposu**:

Bu projenin Docker imajları iki ayrı depoda yayımlanmaktadır, daha hızlı olanı seçin:

- **Docker Hub** (Önerilen):
  - CPU Sürümü: `hgmzhn/manga-translator:latest-cpu`
  - GPU Sürümü: `hgmzhn/manga-translator:latest-gpu`

- **GitHub Container Registry** (Yedek):
  - CPU Sürümü: `ghcr.io/hgmzhn/manga-translator:latest-cpu`
  - GPU Sürümü: `ghcr.io/hgmzhn/manga-translator:latest-gpu`

**Erişim Adresi** (varsayılan port 8000):
- 🌐 Kullanıcı Arayüzü: `http://localhost:8000`
- 🔧 Yönetim Arayüzü: `http://localhost:8000/admin.html`

> 📖 **Ayrıntılı kurulum kılavuzu**: [Docker Dağıtım Belgeleri](doc/INSTALLATION.md)  
> 📖 **Kullanım kılavuzu**: [Komut Satırı Kullanım Kılavuzu](doc/CLI_USAGE.md)

#### Yöntem 4: Kaynak Koddan Çalıştırma (Geliştiriciler)

Geliştiriciler veya özelleştirme yapmak isteyen kullanıcılar için uygundur.

1. **Python 3.12 kurun**: [İndir](https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe)
2. **Depoyu klonlayın**:
   ```bash
   git clone https://github.com/hgmzhn/manga-translator-ui.git
   cd manga-translator-ui
   ```
3. **Bağımlılıkları kurun**:
   ```bash
   # NVIDIA GPU
   pip install -r requirements_gpu.txt
   
   # AMD GPU (yalnızca RX 7000/9000 serisi)
   pip install -r requirements_amd.txt
   
   # CPU Sürümü
   pip install -r requirements_cpu.txt
   ```
4. **Programı çalıştırın**:
   ```bash
   # Masaüstü UI
   python -m desktop_qt_ui.main
   
   # Web UI (isteğe bağlı)
   python -m manga_translator web
   ```

> 📖 **Ayrıntılı kurulum kılavuzu**: [Kurulum Kılavuzu](doc/INSTALLATION.md)  
> 📖 **Kullanım kılavuzu**: [Komut Satırı Kullanım Kılavuzu](doc/CLI_USAGE.md)

#### Yöntem 5: macOS Yerel Çalıştırma (Apple Silicon)

M1/M2/M3/M4 Mac için optimize edilmiş yerel çalıştırma yöntemi, MPS (Metal Performance Shaders) GPU hızlandırmasını destekler.

**Hızlı Başlangıç (Önerilen)**:

1. **Kurulum betiğini indirin**:
   ```bash
   curl -O https://raw.githubusercontent.com/hgmzhn/manga-translator-ui/main/macOS_1_IlkKurulum.sh
   chmod +x macOS_1_IlkKurulum.sh
   ```

2. **Kurulumu çalıştırın**:
   ```bash
   ./macOS_1_IlkKurulum.sh
   ```
   Betik otomatik olarak şunları tamamlar:
   - Gerekli bileşenleri kontrol eder ve kurar (Xcode Komut Satırı Araçları, Git)
   - Proje kodunu klonlar
   - Miniforge ve Python ortamını kurar
   - MPS GPU hızlandırma desteğini yapılandırır

3. **Programı başlatın**:
   ```bash
   ./macOS_2_QtArayuzuBaslat.sh
   ```

4. **Sonraki güncellemeler**:
   ```bash
   ./macOS_4_GuncellemeVeBakim.sh
   ```

**Veya manuel klonlama**:
```bash
git clone https://github.com/hgmzhn/manga-translator-ui.git
cd manga-translator-ui
chmod +x macOS_*.sh
./macOS_1_IlkKurulum.sh
```

> ⚠️ **Not**:
> - Apple Silicon (M1/M2/M3/M4) çipleri öncelikli olarak desteklenir
> - Intel Mac'lerde de çalışır, ancak CPU modu kullanılır
> - İlk kurulum yaklaşık 2GB bağımlılık paketi indirir, internet bağlantınızın sağlam olduğundan emin olun


---

## 📖 Kullanım Kılavuzu

### 🖥️ Qt Arayüzü Modu

Kurulum tamamlandıktan sonra resimleri nasıl çevireceğinizi öğrenmek için kullanım kılavuzuna bakın:

**Kullanım Kılavuzu** → [doc/USAGE.md](doc/USAGE.md)

Temel adımlar:
1. API'yi doldurun (çevrimiçi çevirici kullanıyorsanız) → [API Yapılandırma Kılavuzu](doc/API_CONFIG.md)
2. GPU'yu kapatın (yalnızca CPU sürümü)
3. Çıktı dizinini ayarlayın
4. Resim ekleyin
5. Çevirici seçin
   - İlk kullanım için önerilen: **Yüksek Kaliteli OpenAI** veya **Yüksek Kaliteli Gemini**
   - API Key yapılandırması gerektirir, [API Yapılandırma Kılavuzu](doc/API_CONFIG.md)'na bakın
6. Çeviriyi başlatın

### ⌨️ Komut Satırı Modu

Toplu işleme ve otomasyon betikleri için uygundur:

**Komut Satırı Kılavuzu** → [doc/CLI_USAGE.md](doc/CLI_USAGE.md)

> ⚠️ **Önemli**: Komut satırını kullanmadan önce proje dizininde sanal ortamı etkinleştirin:
> ```bash
> # Windows
> conda activate manga-env
> 
> # Linux/macOS
> conda activate manga-env
> ```

Hızlı başlangıç:
```bash
# Local modu (Önerilen, komut satırı çevirisi)
python -m manga_translator local -i manga.jpg

# Veya kısaca (varsayılan Local modu)
python -m manga_translator -i manga.jpg

# Tüm klasörü çevir
python -m manga_translator local -i ./manga_folder/ -o ./output/

# Web sunucusu modu (yönetim arayüzü ve API ile)
python -m manga_translator web --host 127.0.0.1 --port 8000 --use-gpu

# Tüm parametreleri görüntüle
python -m manga_translator --help
```

---

## 📋 İş Akışları

Bu program birden fazla iş akışını destekler:

1. **Normal Çeviri Akışı** - Resimleri doğrudan çevir 
2. **Çeviriyi Dışa Aktar** - Çeviriden sonra TXT dosyasına aktar
3. **Orijinali Dışa Aktar** - Yalnızca algıla ve tanı, manuel çeviri için orijinali aktar
4. **Çeviriyi İçe Al ve Oluştur** - TXT/JSON'dan çeviri içeriğini içe alıp yeniden oluştur

**İş Akışı Detayları** → [doc/WORKFLOWS.md](doc/WORKFLOWS.md)

---

## ⚙️ Sık Kullanılan Çeviriciler

### Çevrimiçi Çeviriciler (API Key gerektirir)
- **OpenAI** - GPT serisi modelleri kullanır
- **Gemini** - Google Gemini modellerini kullanır
- **Sakura** - Japonca için özel olarak optimize edilmiş çeviri modeli

### Yüksek Kaliteli Çeviriciler (Önerilen)
- **Yüksek Kaliteli OpenAI** - GPT-4o çok modlu modeli kullanır
- **Yüksek Kaliteli Gemini** - Gemini çok modlu modeli kullanır
- 📸 Resim bağlamıyla birleştirilmiş, daha doğru çeviri

**Tam Ayarlar Açıklaması** → [doc/SETTINGS.md](doc/SETTINGS.md)

---

## 🔍 Sorunlarla mı Karşılaştınız?

### Çeviri Sonuçları İstediğiniz Gibi Değil

1. "Temel Ayarlar"da **Ayrıntılı Günlük** seçeneğini işaretleyin
2. `result/` dizinindeki hata ayıklama dosyalarına bakın
3. Algılayıcı ve OCR parametrelerini ayarlayın

**Hata Ayıklama Kılavuzu** → [doc/DEBUGGING.md](doc/DEBUGGING.md)

---

## ⭐ Yıldız Geçmişi

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=hgmzhn/manga-translator-ui&type=Date)](https://star-history.com/#hgmzhn/manga-translator-ui&Date)

</div>

---

## 🙏 Teşekkürler

- [zyddnys/manga-image-translator](https://github.com/zyddnys/manga-image-translator) - Çekirdek çeviri motoru
- [bilibili/ailab](https://github.com/bilibili/ailab) - Real-CUGAN süper çözünürlük modeli
- [the-database/MangaJaNai](https://github.com/the-database/MangaJaNai) - MangaJaNai/IllustrationJaNai süper çözünürlük modeli
- [lhj5426/YSG](https://github.com/lhj5426/YSG) - Model desteği sağlar
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - OCR model desteği sağlar
- [kha-white/manga-ocr](https://github.com/kha-white/manga-ocr) - MangaOCR model desteği
- [jzhang533/PaddleOCR-VL-For-Manga](https://github.com/jzhang533/PaddleOCR-VL-For-Manga) - PaddleOCR-VL-For-Manga model desteği sağlar
- Tüm katkıda bulunanların ve kullanıcıların desteği

---

## 📝 Lisans

Bu proje GPL-3.0 lisansı altında açık kaynaklıdır.

### Model Lisans Bildirimi

Bu projenin kodu **GPL-3.0 lisansını** kullanmaktadır.

Bu proje, görüntü süper çözünürlük işlemi için MangaJaNai/IllustrationJaNai modellerini kullanmayı destekler. Bu model ağırlık dosyaları **CC BY-NC 4.0 lisansını** (Atıf-GayrıTicari 4.0 Uluslararası) kullanmaktadır ve yalnızca ticari olmayan amaçlarla kullanılabilir.

- **Model Kaynağı**: [MangaJaNai](https://github.com/the-database/MangaJaNai)
- **Model Lisansı**: CC BY-NC 4.0
- **Kullanım Kısıtlaması**: Yalnızca ticari olmayan amaçlar

---

## ⚠️ Özel Bildirim

Bu proje yalnızca teknik tanıtım ve kişisel öğrenme/paylaşım amaçlı sunulmaktadır; herhangi bir hukuki, ticari veya uyumluluk tavsiyesi oluşturmamaktadır.  
Projenin ilgili işlevlerini kurarken, yapılandırırken, çağırırken ve dağıtırken bulunduğunuz yerdeki yasa ve yönetmeliklere, platform kurallarına, içerik kaynağı lisanslarına ve üçüncü taraf hizmet koşullarına kendi sorumluluğunuzda uymanız gerekmektedir.

### Sorumluluk Reddi ve Sınırlaması

- Bu projenin kullanımından kaynaklanan tüm eylem ve sonuçlardan (içerik işleme, yayımlama, dağıtma, yeniden dağıtma, ticari kullanım dahil ancak bunlarla sınırlı olmamak üzere) kullanıcı bağımsız olarak sorumludur.
- Girdi içeriğinin, çıktı içeriğinin ve veri kaynaklarının yasal yetkiye sahip olduğundan emin olmalısınız; telif hakkı, marka, gizlilik, kişilik hakları ve diğer yasal hakları ihlal eden senaryolarda kullanılamaz.
- Bu projeyi korsanlık yayma, yetkisiz toplu veri çekme ve taşıma, platform kısıtlamalarını aşma, dolandırıcılık, iftira, başkalarının yasal haklarına zarar verme dahil herhangi bir yasa dışı amaçla kullanmak kesinlikle yasaktır.
- Bu proje üçüncü taraf modellere, API'lere, verilere ve kütüphanelere (OCR, çeviri, süper çözünürlük modelleri dahil) bağımlıdır; ilgili kullanılabilirlik, doğruluk, kararlılık, maliyet, risk kontrolü ve uyumluluk gereksinimleri ilgili hizmet sağlayıcının sorumluluğundadır ve kullanıcı ilgili riskleri ve maliyetleri kabul etmek zorundadır.
- Bu projenin kullanılması veya kullanılamamasından kaynaklanan doğrudan veya dolaylı kayıplar (veri kaybı, iş kesintisi, gelir kaybı, hesap riski, üçüncü taraf talepleri dahil ancak bunlarla sınırlı olmamak üzere) için proje yazarları ve katkıda bulunanlar, yürürlükteki yasaların izin verdiği ölçüde sorumluluk kabul etmemektedir.
- Bu projeyi ekip veya kurumsal ortamda kullanıyorsanız, izin yönetimi, günlük denetimi, içerik incelemesi ve uyumluluk değerlendirmesini kendi sorumluluğunuzda gerçekleştirmeniz ve gerekli manuel inceleme süreçlerini oluşturmanız gerekmektedir.

Kullanmadan önce riskleri dikkatli değerlendirin; kullanmaya devam etmeniz yukarıdaki bildirimi okuduğunuzu, anladığınızı ve kabul ettiğinizi gösterir.

---