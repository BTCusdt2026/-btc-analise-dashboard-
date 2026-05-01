import pandas as pd
import requests
from datetime import datetime

def get_data(symbol, interval):
    """Pega candles reais da Binance"""
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": f"{symbol}USDT", "interval": interval, "limit": 200}
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    
    df = pd.DataFrame(data, columns=[
        'timestamp','open','high','low','close','volume','close_time',
        'qav','trades','tb_base','tb_quote','ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
    return df

def get_preco(symbol):
    """Pega preço atual em tempo real"""
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    r
