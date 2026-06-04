"""Helper functions for the trading bot."""
import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    """Get configuration from environment variables."""
    config = {
        'telegram_token': os.getenv('TELEGRAM_TOKEN'),
        'binance_api_key': os.getenv('BINANCE_API_KEY'),
        'binance_api_secret': os.getenv('BINANCE_API_SECRET'),
        'database_path': os.getenv('DATABASE_PATH', 'trading_bot.db'),
        'default_timeframe': os.getenv('DEFAULT_TIMEFRAME', '1h'),
        'rsi_period': int(os.getenv('RSI_PERIOD', 14)),
        'rsi_overbought': int(os.getenv('RSI_OVERBOUGHT', 70)),
        'rsi_oversold': int(os.getenv('RSI_OVERSOLD', 30)),
        'macd_fast': int(os.getenv('MACD_FAST', 12)),
        'macd_slow': int(os.getenv('MACD_SLOW', 26)),
        'macd_signal': int(os.getenv('MACD_SIGNAL', 9)),
        'bollinger_bands_period': int(os.getenv('BOLLINGER_BANDS_PERIOD', 20)),
        'bollinger_bands_std': float(os.getenv('BOLLINGER_BANDS_STD', 2)),
        'tracking_symbols': os.getenv('TRACKING_SYMBOLS', 'BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT').split(','),
        'update_interval': int(os.getenv('UPDATE_INTERVAL', 300)),
        'send_notifications': os.getenv('SEND_NOTIFICATIONS', 'true').lower() == 'true',
        'strong_signal_threshold': float(os.getenv('STRONG_SIGNAL_THRESHOLD', 0.8)),
    }
    
    # Validate required config
    if not config['telegram_token']:
        raise ValueError('TELEGRAM_TOKEN not set in environment variables')
    if not config['binance_api_key']:
        raise ValueError('BINANCE_API_KEY not set in environment variables')
    if not config['binance_api_secret']:
        raise ValueError('BINANCE_API_SECRET not set in environment variables')
    
    return config

def format_price(price):
    """Format price for display."""
    if price >= 1:
        return f'${price:,.2f}'
    else:
        return f'${price:.8f}'

def format_percentage(value):
    """Format percentage for display."""
    return f'{value:.2f}%'

def format_signal_strength(strength):
    """Format signal strength with emoji."""
    if strength >= 0.8:
        return '🔴 Güçlü' if strength > 0 else '🟢 Güçlü'
    elif strength >= 0.5:
        return '🟠 Orta' if strength > 0 else '🟡 Orta'
    else:
        return '🟡 Zayıf' if strength > 0 else '⚪ Zayıf'
