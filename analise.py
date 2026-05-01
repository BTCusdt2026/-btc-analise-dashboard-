import pandas as pd
import requests
from datetime import datetime

COIN_MAP = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "BNB": "binancecoin", "XRP": "ripple"}

def get_data(symbol, interval):
    """Pega candles reais da CoinGecko com /market_chart"""
    coin_id = COIN_MAP.get(symbol, "bitcoin")
    
    # Mapeia timeframe pra dias + intervalo
    interval_map = {
        "1m": {"days": "1", "interval": "minute"},
        "5m": {"days": "1", "interval": "minute"}, 
        "15m": {"days": "1", "interval": "minute"},
        "1h": {"days": "1", "interval": "hourly"},
        "4h": {"days": "1", "interval": "hourly"},
        "1d": {"days": "200", "interval": "daily"}
    }
    
    cfg = interval_map.get(interval, {"days": "1", "interval": "hourly"})
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": cfg["days"], "interval": cfg["interval"]}
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        # market_chart retorna {prices: [[ts, price]], volumes: [[ts, vol]]}
        prices = data['prices']
        volumes = data['volumes']
        
        df = pd.DataFrame(prices, columns=['timestamp', 'close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['volume'] = [v[1] for v in volumes]
        
        # Para OHLC simulamos open/high/low = close, já que CoinGecko não dá OHLC no intraday
        df['open'] = df['close'].shift(1).fillna(df['close'])
        df['high'] = df[['open', 'close']].max(axis=1)
        df['low'] = df[['open', 'close']].min(axis=1)
        
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except Exception as e:
        raise Exception(f"CoinGecko erro: {e}")

def get_preco(symbol):
    """Preço atual em tempo real"""
    coin_id = COIN_MAP.get(symbol, "bitcoin")
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id, "vs_currencies": "usd"}
    r = requests.get(url, timeout=5)
    return float(r.json()[coin_id]['usd'])

def calcular_indicadores(df):
    """Calcula RSI e MACD reais"""
    if df.empty:
        return df
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()
    df['macd'] = ema12 - ema26
    return df
