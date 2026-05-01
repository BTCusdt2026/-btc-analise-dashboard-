import requests

BASE = "https://fapi.binance.com"

def get_price():
    r = requests.get(f"{BASE}/fapi/v1/ticker/price?symbol=BTCUSDT")
    return float(r.json()["price"])

def get_open_interest():
    r = requests.get(f"{BASE}/fapi/v1/openInterest?symbol=BTCUSDT")
    return float(r.json()["openInterest"])
