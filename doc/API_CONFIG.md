# API Yapilandirma Kilavuzu

Bu belge yaygin cevrimici ceviri API'lerinin basvurusu ve yapilandirma kilavuzunu saglar.

---

## Icindekiler

- [Model Secim Onerileri](#model-secim-onerileri)
- [Genel API Yapilandirma Aciklamasi](#genel-api-yapilandirma-aciklamasi)
- [SiliconFlow API Yapilandirmasi](#siliconflow-api-yapilandirmasi)
- [DeepSeek API Yapilandirmasi](#deepseek-api-yapilandirmasi)
- [Google Gemini API Yapilandirmasi](#google-gemini-api-yapilandirmasi)
- [Sik Sorulan Sorular](#sik-sorulan-sorular)

---

## Model Secim Onerileri

- **Yuksek Kaliteli Ceviriciler** cok modlu modeller gerektirir (gorsel "gorebilen" AI); Grok, Gemini, ChatGPT gibi modeller manga sahnelerini gorebilir ve daha dogru ceviri yapabilir
- Genel olarak parametre sayisi daha buyuk olan modeller daha iyi ceviri sonuclari verir

### Parametre Sayisini Nasil Okursunuz

Model adlari genellikle parametre bilgisi icerir, ornegin:
- `Qwen3-235B` -> 235 milyar parametre
- `DeepSeek-V3-671B` -> 671 milyar parametre
- `Llama-3-70B` -> 70 milyar parametre

Parametre birimi: `B` = Billion (milyar)

### Cok Modlu Model Ornekleri

| Model | Platform | Aciklama |
|-------|----------|----------|
| `gpt-5.2` | OpenAI | ChatGPT en son cok modlu |
| `gemini-3-pro-preview` | Google | Gemini en son cok modlu |
| `gemini-2.5-pro` | Google | Gemini cok modlu |
| `grok-4.1` | xAI | Grok en son cok modlu |

### Duz Metin Modeli Ornekleri

| Model | Platform | Aciklama |
|-------|----------|----------|
| `deepseek-chat` | DeepSeek | Hizli |
| `deepseek-reasoner` | DeepSeek | Dusunme vardir, satir sonu kararlı |
| `Qwen/Qwen3-235B-A22B` | SiliconFlow | Tongyi Qianwen 3, 235 milyar parametre |

---

## Genel API Yapilandirma Aciklamasi

### Cevirici Turleri

Program iki tur cevirici saglar; farklari yalnizca **arayuzlerindedir**:

#### Standart Cevirici (OpenAI / Gemini)
- Duz metin API kullanir
- Yalnizca tanilan metni gonderir
- Ceviri hizi hizli, tüketim az
- Basit senaryolar icin uygundur

#### Yuksek Kaliteli Cevirici (Yuksek Kaliteli OpenAI / Yuksek Kaliteli Gemini)
- Cok modlu API kullanir (gorsel destekler)
- Gorsel + metin gonderir
- AI gorsel "gorebilir" ve sahneyi anlar
- Daha dogru ceviri, ancak daha fazla tuketir
- **Cok modlu model gerektirir** (GPT-4o, Gemini gibi)

> Modeliniz cok modali destekliyorsa en iyi sonuc icin "Yuksek Kaliteli Cevirici" kullanmaniz kesinlikle onerilir!

### API Adresini Doldurma Kurallari

#### OpenAI Uyumlu Arayuz

OpenAI ceviricisi piyasadaki **neredeyse tum modelleri destekler**; hemen hemen tum AI platformlari OpenAI uyumlu arayuz saglar.

- **Genel Durum**: API adresi `/v1` ile biter
  - Ornek: `https://api.openai.com/v1`
  - Ornek: `https://api.deepseek.com/v1`
  - Desteklenir: DeepSeek, Groq, Together AI, OpenRouter, **SiliconFlow**, **Volcano Engine** vb.
- **Istisna Durum**: Bazi servis saglayicilari farkli surum numarasi kullanabilir

> API saglayiciniz OpenAI uyumlu arayuz destekliyorsa OpenAI ceviricisini kullanabilirsiniz!

#### Gemini Arayuzu
- **Surum numarasi eklemenize gerek yok**: Temel adresi dogrudan girin
  - Girin: `https://generativelanguage.googleapis.com`
  - Program otomatik `/v1beta` ekler
- **AI Studio resmi anahtari kullaniyorsaniz**: API adresini doldurmaya gerek yok (varsayilan adres otomatik kullanilir)

---

## SiliconFlow API Yapilandirmasi

SiliconFlow yurt ici bir AI platformudur; birden fazla model saglar, yeni kullanicilar ucretsiz kredi alir, fiyati ucuzdur ve yurt ici erisim hizlidir.

> Avantaj: Yeni kullanici kaydinda ucretsiz kredi verilir; Qwen3, DeepSeek ve diger modeller desteklenir; proxy gerekmeksizin dogrudan baglanilabilir.

### 1. Hesap Olusturun

1. [SiliconFlow Resmi Sitesi](https://cloud.siliconflow.cn/) adresini ziyaret edin
2. "Kayit Ol" dugmesine tiklayin ve telefon numarasiyla kaydolun
3. Dogrulama islemini tamamlayin

### 2. API Key Olusturun

1. Giris yapip konsola gidin
2. Sol taraftaki "API Anahtarlari" bolumune tiklayin
3. "Yeni API Anahtari" dugmesine tiklayin
4. Olusturulan API Key'i kopyalayin

### 3. Programa Yapilandirin

1. Programi acin
2. "Temel Ayarlar" -> "Cevirici" bolumunden "OpenAI" secin
3. "Gelismis Ayarlar"da doldurun:
   - **API Key**: SiliconFlow API Key'iniz
   - **Taban URL**: `https://api.siliconflow.cn/v1`
   - **Model**: [Model Marketi](https://cloud.siliconflow.cn/models) adresinde tum kullanilabilir modelleri goruntuleyin

---

## DeepSeek API Yapilandirmasi

DeepSeek yuksek kaliteli, dusuk maliyetli AI ceviri hizmeti saglar; manga cevirisi icin cok uygundur.

> Not: DeepSeek cok modali desteklemez; "Yuksek Kaliteli Cevirici" kullanilamaz. En iyi ceviri sonucu icin cok modlu modeller (OpenAI GPT-4o, Google Gemini gibi) kullanmaniz onerilir.

### 1. Hesap Olusturun

1. [DeepSeek Acik Platform](https://platform.deepseek.com/) adresini ziyaret edin
2. "Kayit Ol" dugmesine tiklayin; e-posta veya telefon numarasiyla kaydolun
3. E-posta dogrulamasini tamamlayin

### 2. Bakiye Yukleme

1. Giris yaptiktan sonra sag ust kosedeki avatara tiklayin -> "Bakiye Yukle"
2. Yuklenecek miktari secin (en az 10 CNY onerilir)
3. Alipay veya WeChat ile odeyin

### 3. API Key Olusturun

1. Sol menuden "API Keys" bolumune tiklayin
2. "API Key Olustur" dugmesine tiklayin
3. Ad girin (ornegin "manga-ceviri")
4. Olusturulan API Key'i kopyalayin (bicim: `sk-xxxxxxxxxxxxxxxx`)
5. Onemli: API Key'i hemen kaydedin; pencereyi kapattiktan sonra tekrar goruntulenemez

### 4. Programa Yapilandirin

1. Programi acin
2. "Temel Ayarlar" -> "Cevirici" bolumunden "OpenAI" secin
3. "Gelismis Ayarlar"da doldurun:
   - **API Key**: DeepSeek API Key'inizi girin (`sk-xxxxxxxxxxxxxxxx`)
   - **Taban URL**: `https://api.deepseek.com/v1` girin
   - **Model**: Asagidaki ikisinden birini secin:
     - `deepseek-chat`: Dusunme yok, hizli, **ancak AI satir sonu calismamasına neden olabilir**
     - `deepseek-reasoner`: Dusunme var, yavas, **ancak satir sonu kararlı ve guvenilir** (Onerilen)

> AI satir sonu islevi uzun metni akillica bolebilir ve balon tasmasini onler. En iyi ceviri sonucu icin `deepseek-reasoner` kullanmaniz onerilir.

---

## Google Gemini API Yapilandirmasi

Google Gemini, Google'in en yeni cok modlu AI modelidir; guclu performans saglar.

> Not: Google AI Studio artik tamamen ucretli olup ucretsiz kredi saglamaz.

### 1. API Key Alin

1. [Google AI Studio](https://aistudio.google.com/apikey) adresini ziyaret edin
2. Google hesabinizla giris yapin
3. "Create API Key" dugmesine tiklayin
4. Google Cloud projesi secin (veya yeni proje olusturun)
5. Olusturulan API Key'i kopyalayin

### 2. Programa Yapilandirin

1. Programi acin
2. "Temel Ayarlar" -> "Cevirici" bolumunden "Yuksek Kaliteli Gemini" veya "Gemini" secin
3. "Gelismis Ayarlar"da doldurun:
   - **API Key**: Gemini API Key'iniz
   - **Taban URL**: Doldurmaya gerek yok (varsayilan adres otomatik kullanilir)
   - **Model**:
     - `gemini-2.5-pro`: Satir sonu kararlı, en yuksek kalite (Onerilen)
     - `gemini-2.5-flash`: Hizli, daha ucuz

---

## Sik Sorulan Sorular

### S1: Hangi API en cok onerilir?

**Cevap**:
- **En Iyi Fiyat/Performans Orani**: DeepSeek
- **En Yuksek Kalite**: OpenAI GPT-4o / Google Gemini

### S2: API Key sizintisi olursa ne yapmaliyim?

**Cevap**:
1. Hemen ilgili platformda sizintili API Key'i silin
2. Yeni bir API Key olusturun
3. Hesap bakiyesini kontrol edin

### S3: "API Key gecersiz" uyarisi alirsam ne yapmaliyim?

**Cevap**:
1. API Key'in tam kopyalanip kopyalanmadigini kontrol edin
2. Taban URL'nin dogru olup olmadigini kontrol edin
3. Hesap bakiyesinin yeterli oldugunu dogrulayin
4. Ag baglantisini kontrol edin (yurt disi API'leri proxy gerektirebilir)

---

[Ana Sayfa](../README.md)'ya don | [Kullanim Kilavuzu](USAGE.md)'na don