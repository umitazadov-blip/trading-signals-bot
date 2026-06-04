# 📊 Trading Signals Bot - Pocket Option Analyzer

Telegram'da çalışan profesyonel bir trading analiz botu. Teknik analiz sinyalleri, al/sat önerileri ve portföy yönetimi özellikleri ile.

## 🎯 Özellikler

- ✅ **Gerçek Zamanlı Fiyat Takibi** - Binance API ile canlı veriler
- ✅ **Teknik Analiz** - RSI, MACD, Bollinger Bands, EMA, SMA
- ✅ **Al/Sat Sinyalleri** - Otomatik analiz ve öneriler
- ✅ **Portföy Yönetimi** - İşlemleri takip et ve analiz et
- ✅ **Özelleştirilebilir Ürünler** - Hangi kripto/hisse istersen analiz et
- ✅ **Bildirimler** - Önemli sinyaller için anında uyarı
- ✅ **İstatistikler** - Kazanç/kayıp analizi
- ✅ **Veritabanı** - SQLite ile lokal veri saklama

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip (Python paket yöneticisi)

### Adım 1: Repository'yi Clone Edin
```bash
git clone https://github.com/umitazadov-blip/trading-signals-bot.git
cd trading-signals-bot
```

### Adım 2: Sanal Ortam Oluşturun
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: Konfigürasyon Dosyasını Düzenleyin
```bash
cp config.example.env config.env
```

`config.env` dosyasını açıp kendi tokenlarınızı girin:
```
TELEGRAM_TOKEN=your_bot_token_here
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

### Adım 5: Botu Çalıştırın
```bash
python main.py
```

## 📱 Telegram Bot Komutları

```
/start          - Botu başlat
/help           - Yardım menüsü
/analyze        - Seçili ürünleri analiz et
/portfolio      - Portföyünü gör
/add_trade      - Yeni işlem ekle
/stats          - İstatistikleri gör
/settings       - Ayarları değiştir
/status         - Bot durumunu kontrol et
```

## 🔧 API Anahtarlarını Nasıl Alırsınız?

### Telegram Bot Token
1. Telegram'da @BotFather'a yazın
2. `/newbot` komutunu girin
3. Bot adını belirleyin
4. Token'ı kopyalayın

### Binance API Anahtarları
1. https://www.binance.com adresine gidin
2. Hesabınıza giriş yapın
3. API Management → Create API Key
4. API Key ve Secret'ı kopyalayın

## 📊 Proje Yapısı

```
trading-signals-bot/
├── main.py                 # Bot'un ana dosyası
├── config.example.env      # Konfigürasyon şablonu
├── requirements.txt        # Python bağımlılıkları
├── README.md              # Bu dosya
│
├── bot/
│   ├── __init__.py
│   ├── telegram_handler.py # Telegram işlemleri
│   └── commands.py         # Bot komutları
│
├── analysis/
│   ├── __init__.py
│   ├── technical.py        # Teknik analiz
│   ├── signals.py          # Al/Sat sinyalleri
│   └── indicators.py       # İndikatörler
│
├── data/
│   ├── __init__.py
│   ├── binance_api.py      # Binance veri çekme
│   └── price_fetcher.py    # Fiyat güncelleme
│
├── database/
│   ├── __init__.py
│   ├── db.py               # Veritabanı işlemleri
│   └── models.py           # Veri modelleri
│
└── utils/
    ├── __init__.py
    ├── logger.py           # Loglama
    └── helpers.py          # Yardımcı fonksiyonlar
```

## 🔐 Güvenlik Notları

- **Hiçbir zaman** API anahtarlarınızı GitHub'a commitlemeyin
- `config.env` dosyasını `.gitignore`'a ekleyin
- Production'da güvenli bir şekilde token saklamak için ortam değişkenleri kullanın
- Bot tokeninizi gizli tutun

## 📝 Lisans

MIT License

## 💡 Katkılar

Bu proje kişisel kullanım için yapılmıştır.

## 📞 Destek

Sorunuz varsa GitHub Issues'da açabilirsiniz.

---

**⚠️ Dikkat:** Bu bot eğitim ve kişisel analiz amaçlıdır. Finansal tavsiye değildir. Yatırım kararlarınızı kendi sorumluluğunuzda alın.