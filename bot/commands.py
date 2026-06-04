from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.helpers import get_config, format_price, format_percentage, format_signal_strength
from utils.logger import setup_logger
from data.binance_api import BinanceAPI
from analysis.signals import SignalGenerator
from database.db import Database

logger = setup_logger(__name__)
config = get_config()
binance = BinanceAPI(config['binance_api_key'], config['binance_api_secret'])
signal_gen = SignalGenerator(config)
db = Database(config['database_path'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler."""
    user = update.effective_user
    await update.message.reply_text(
        f"🎉 Hoşgeldiniz {user.first_name}!\n\n"
        "📊 Pocket Option Trading Bot'a hoşgeldiniz.\n"
        "Kripto ve forex piyasalarını teknik analiz ile analiz ediyorum.\n\n"
        "/help - Komutları görmek için\n"
        "/analyze - Seçili ürünleri analiz et\n"
        "/portfolio - Portföyünüzü görün",
        parse_mode='HTML'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler."""
    help_text = """
📚 <b>Komutlar</b>

/start - Botu başlat
/help - Bu yardım menüsü
/analyze - Seçili ürünleri analiz et
/portfolio - Açık işlemlerinizi görmek
/add_trade - Yeni işlem ekle
/stats - Trading istatistiklerinizi görmek
/settings - Bot ayarlarını değiştir
/status - Bot durumunu kontrol et

<b>Teknik İndikatörler:</b>
• RSI (Relative Strength Index)
• MACD (Moving Average Convergence Divergence)
• Bollinger Bands
• EMA (Exponential Moving Average)
• SMA (Simple Moving Average)

<b>Sinyaller:</b>
🟢 BUY - Satın alma sinyali
🔴 SELL - Satış sinyali
⚪ NEUTRAL - Nötr sinyal
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze market command."""
    symbols = config['tracking_symbols']
    
    await update.message.reply_text("📊 Analiz ediliyor...", parse_mode='HTML')
    
    analysis_text = "<b>📊 Teknik Analiz Sonuçları</b>\n\n"
    
    for symbol in symbols:
        try:
            # Get price data
            klines = binance.get_klines(symbol, '1h', 100)
            if not klines:
                continue
            
            prices = [float(k[4]) for k in klines]  # Close prices
            current_price = prices[-1]
            
            # Generate signal
            signal = signal_gen.generate_signal(prices)
            
            if signal:
                analysis_text += f"<b>{symbol}</b>\n"
                analysis_text += f"Fiyat: {format_price(current_price)}\n"
                analysis_text += f"Sinyal: {signal['type']} {format_signal_strength(signal['strength'])}\n"
                analysis_text += f"RSI: {signal['rsi']:.2f}\n"
                analysis_text += f"Güç: {format_percentage(signal['strength'] * 100)}\n"
                
                for reason in signal['reasons']:
                    analysis_text += f"  • {reason}\n"
                
                analysis_text += "\n"
        
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            continue
    
    await update.message.reply_text(analysis_text, parse_mode='HTML')

async def portfolio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show portfolio."""
    trades = db.get_open_trades()
    
    if not trades:
        await update.message.reply_text("📈 Açık işleminiz yok.", parse_mode='HTML')
        return
    
    portfolio_text = "<b>📈 Portföy</b>\n\n"
    
    for trade in trades:
        portfolio_text += f"<b>{trade[1]}</b> - {trade[7]}\n"
        portfolio_text += f"Giriş: {format_price(trade[2])}\n"
        portfolio_text += f"Tarih: {trade[3]}\n\n"
    
    await update.message.reply_text(portfolio_text, parse_mode='HTML')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show trading statistics."""
    stats = db.get_trade_stats()
    
    if stats['total'] == 0:
        await update.message.reply_text("📊 Henüz işlem yok.", parse_mode='HTML')
        return
    
    win_rate = (stats['wins'] / stats['total'] * 100) if stats['total'] > 0 else 0
    
    stats_text = f"""
<b>📊 Trading İstatistikleri</b>

Toplam İşlem: {stats['total']}
Kazanan: {stats['wins']}
Kazanç Oranı: {win_rate:.2f}%
Toplam Kar: {format_price(stats['profit'])}
"""
    
    await update.message.reply_text(stats_text, parse_mode='HTML')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check bot status."""
    try:
        ticker = binance.get_24h_ticker('BTCUSDT')
        
        status_text = f"""
<b>🤖 Bot Durumu</b>

Status: ✅ Çalışıyor
API Bağlantısı: ✅ Bağlı
Bitcoin Fiyatı: {format_price(float(ticker['lastPrice']))}
24h Değişim: {format_percentage(float(ticker['priceChangePercent']))}
"""
        await update.message.reply_text(status_text, parse_mode='HTML')
    
    except Exception as e:
        await update.message.reply_text(f"❌ Hata: {str(e)}", parse_mode='HTML')
