import requests

BASE = "https://fapi.binance.com"

def price():
    r = requests.get(f"{BASE}/fapi/v1/ticker/price?symbol=BTCUSDT")
    return float(r.json()["price"])

def open_interest():
    r = requests.get(f"{BASE}/fapi/v1/openInterest?symbol=BTCUSDT")
    return float(r.json()["openInterest"])
