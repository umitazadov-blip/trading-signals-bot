from binance.client import Client
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        logger.info('Binance API initialized')
    
    def get_current_price(self, symbol):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logger.error(f'Error fetching price for {symbol}: {e}')
            return None
    
    def get_klines(self, symbol, interval, limit=100):
        try:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            return klines
        except Exception as e:
            logger.error(f'Error fetching klines: {e}')
            return None
    
    def get_24h_ticker(self, symbol):
        try:
            ticker = self.client.get_ticker(symbol=symbol)
            return ticker
        except Exception as e:
            logger.error(f'Error fetching ticker: {e}')
            return None
