import pandas as pd
import yfinance as yf
from datetime import datetime

SYMBOL_MAP = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "BNB": "BNB-USD", "XRP": "XRP-USD"}

def get_data(symbol, interval):
    """Pega candles reais do Yahoo Finance"""
    ticker = SYMBOL_MAP.get(symbol, "BTC-USD")
    
    # yfinance usa: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    interval_map = {
        "1m": "1m", "5m": "5m", "15m": "15m", 
        "1h": "1h", "4h": "1h", "1d": "1d"
    }
    yf_interval = interval_map.get(interval, "1h")
    
    # period = 1d pra intraday, 200d pra 1d
    period = "1d" if yf_interval != "1d" else "200d"
    
    try:
        df = yf.download(ticker, period=period, interval=yf_interval, progress=False)
        if df.empty:
            raise Exception("yfinance retornou vazio")
        
        df = df.reset_index()
        df = df.rename(columns={"Datetime": "timestamp", "Date": "timestamp", "Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except Exception as e:
        raise Exception(f"yfinance erro: {e}")

def get_preco(symbol):
    """Preço atual em tempo real"""
    ticker = SYMBOL_MAP.get(symbol, "BTC-USD")
    df = yf.download(ticker, period="1d", interval="1m", progress=False)
    return float(df['Close'].iloc[-1])

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
