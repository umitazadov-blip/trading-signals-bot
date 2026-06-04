import sqlite3
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)

class Database:
    def __init__(self, db_path='trading_bot.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                entry_price REAL NOT NULL,
                entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                exit_price REAL,
                exit_time TIMESTAMP,
                type TEXT NOT NULL,
                status TEXT DEFAULT 'open',
                profit REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                strength REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logger.info('Database initialized')
    
    def add_trade(self, symbol, entry_price, trade_type):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO trades (symbol, entry_price, type, status) VALUES (?, ?, ?, "open")', (symbol, entry_price, trade_type))
        conn.commit()
        trade_id = cursor.lastrowid
        conn.close()
        return trade_id
    
    def get_open_trades(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trades WHERE status = "open" ORDER BY entry_time DESC')
        trades = cursor.fetchall()
        conn.close()
        return trades
    
    def get_trade_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM trades WHERE status = "closed"')
        total = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM trades WHERE status = "closed" AND profit > 0')
        wins = cursor.fetchone()[0]
        cursor.execute('SELECT SUM(profit) FROM trades WHERE status = "closed"')
        profit = cursor.fetchone()[0] or 0
        conn.close()
        return {'total': total, 'wins': wins, 'profit': profit}
