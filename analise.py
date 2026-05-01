import pandas as pd
import requests
from datetime import datetime

def get_data(symbol, interval):
    """Pega candles reais da CoinGecko"""
    coin_map = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "BNB": "binancecoin", "XRP": "ripple"}
    coin_id = coin_map.get(symbol, "bitcoin")
    
    # CoinGecko usa dias. 1m=1, 5m=1, 15m=1, 1h=1, 4h=1, 1d=200
    days = "1" if interval != "1d" else "200"
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {"vs_currency": "usd", "days": days}
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        # CoinGecko retorna [timestamp, open, high, low, close]
        df = pd.DataFrame(data, columns=['timestamp','open','high','low','close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df[['open','high','low','close']] = df[['open','high','low','close']].astype(float)
        
        # Se for timeframe menor que 1d, CoinGecko só tem 1 dia. Então simula volume
        df['volume'] = df['close'] * 1000  
        return df
    except Exception as e:
        raise Exception(f"CoinGecko erro: {e}")

def get_preco(symbol):
    """Pega preço atual em tempo real da CoinGecko"""
    coin_map = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana", "BNB": "binancecoin", "XRP": "ripple"}
    coin_id = coin_map.get(symbol, "bitcoin")
    
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
