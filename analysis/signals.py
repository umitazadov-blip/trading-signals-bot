from utils.logger import setup_logger
from .indicators import Indicators

logger = setup_logger(__name__)

class SignalGenerator:
    def __init__(self, config):
        self.config = config
        self.indicators = Indicators(config)
    
    def generate_signal(self, prices):
        if len(prices) < 100:
            logger.warning('Not enough price data for signal generation')
            return None
        
        rsi = self.indicators.calculate_rsi(prices)
        macd = self.indicators.calculate_macd(prices)
        bollinger = self.indicators.calculate_bollinger_bands(prices)
        ema_20 = self.indicators.calculate_ema(prices, 20)
        ema_50 = self.indicators.calculate_ema(prices, 50)
        
        signal_strength = 0
        signal_type = 'NEUTRAL'
        reasons = []
        
        if rsi is not None:
            if rsi < self.config['rsi_oversold']:
                signal_strength += 0.25
                signal_type = 'BUY'
                reasons.append(f'RSI oversold: {rsi:.2f}')
            elif rsi > self.config['rsi_overbought']:
                signal_strength -= 0.25
                signal_type = 'SELL'
                reasons.append(f'RSI overbought: {rsi:.2f}')
        
        if macd['histogram'] > 0 and macd['macd'] > macd['signal']:
            signal_strength += 0.25
            if signal_type != 'SELL':
                signal_type = 'BUY'
            reasons.append('MACD bullish')
        elif macd['histogram'] < 0 and macd['macd'] < macd['signal']:
            signal_strength -= 0.25
            signal_type = 'SELL'
            reasons.append('MACD bearish')
        
        current_price = prices[-1]
        if current_price <= bollinger['lower']:
            signal_strength += 0.25
            if signal_type != 'SELL':
                signal_type = 'BUY'
            reasons.append('Price at lower Bollinger Band')
        elif current_price >= bollinger['upper']:
            signal_strength -= 0.25
            signal_type = 'SELL'
            reasons.append('Price at upper Bollinger Band')
        
        if ema_20 > ema_50:
            signal_strength += 0.25
            if signal_type != 'SELL':
                signal_type = 'BUY'
            reasons.append('EMA 20 > EMA 50 (Bullish trend)')
        elif ema_20 < ema_50:
            signal_strength -= 0.25
            signal_type = 'SELL'
            reasons.append('EMA 20 < EMA 50 (Bearish trend)')
        
        signal_strength = max(0, min(1, (signal_strength + 1) / 2))
        
        return {
            'type': signal_type,
            'strength': signal_strength,
            'reasons': reasons,
            'rsi': rsi,
            'macd': macd,
            'bollinger': bollinger,
            'ema_20': ema_20,
            'ema_50': ema_50
        }
    
    def is_strong_signal(self, signal):
        if signal is None:
            return False
        return signal['strength'] >= self.config['strong_signal_threshold']
