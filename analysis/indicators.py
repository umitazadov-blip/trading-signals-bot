import pandas as pd
import numpy as np

class Indicators:
    def __init__(self, config):
        self.config = config
    
    def calculate_rsi(self, prices, period=None):
        if period is None:
            period = self.config['rsi_period']
        
        if len(prices) < period:
            return None
        
        delta = pd.Series(prices).diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1]
    
    def calculate_macd(self, prices):
        series = pd.Series(prices)
        fast = series.ewm(span=self.config['macd_fast']).mean()
        slow = series.ewm(span=self.config['macd_slow']).mean()
        
        macd_line = fast - slow
        signal_line = macd_line.ewm(span=self.config['macd_signal']).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line.iloc[-1],
            'signal': signal_line.iloc[-1],
            'histogram': histogram.iloc[-1]
        }
    
    def calculate_bollinger_bands(self, prices):
        period = self.config['bollinger_bands_period']
        std = self.config['bollinger_bands_std']
        
        series = pd.Series(prices)
        sma = series.rolling(window=period).mean()
        std_dev = series.rolling(window=period).std()
        
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        
        return {
            'upper': upper_band.iloc[-1],
            'middle': sma.iloc[-1],
            'lower': lower_band.iloc[-1],
            'current_price': prices[-1]
        }
    
    def calculate_ema(self, prices, period):
        series = pd.Series(prices)
        ema = series.ewm(span=period).mean()
        return ema.iloc[-1]
    
    def calculate_sma(self, prices, period):
        series = pd.Series(prices)
        sma = series.rolling(window=period).mean()
        return sma.iloc[-1]
