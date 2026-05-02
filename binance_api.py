import requests

BASE_URL = "https://fapi.binance.com"

def get_price(symbol="BTCUSDT"):
    url = f"{BASE_URL}/fapi/v1/ticker/price"
    params = {"symbol": symbol}
    data = requests.get(url, params=params).json()
    return float(data["price"])

def get_open_interest(symbol="BTCUSDT"):
    url = f"{BASE_URL}/futures/data/openInterestHist"
    params = {
        "symbol": symbol,
        "period": "5m",
        "limit": 2
    }
    data = requests.get(url, params=params).json()
    
    if len(data) < 2:
        return 0
    
    last = float(data[-1]["sumOpenInterest"])
    prev = float(data[-2]["sumOpenInterest"])
    
    return last - prev
