from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="Radar Institucional BTC")
templates = Jinja2Templates(directory="templates")

BASE_URL = "https://fapi.binance.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_price(symbol="BTCUSDT"):
    try:
        r = requests.get(f"{BASE_URL}/fapi/v1/ticker/price", params={"symbol": symbol}, headers=HEADERS, timeout=5)
        return float(r.json()["price"])
    except:
        return 0.0

def get_open_interest(symbol="BTCUSDT"):
    try:
        r = requests.get(f"{BASE_URL}/futures/data/openInterestHist", params={"symbol": symbol, "period": "5m", "limit": 2}, headers=HEADERS, timeout=5)
        data = r.json()
        if len(data) < 2: 
            return 0
        return float(data[-1]["sumOpenInterest"]) - float(data[-2]["sumOpenInterest"])
    except:
        return 0

def institutional_signal(symbol="BTCUSDT"):
    try:
        price = get_price(symbol)
        oi_delta = get_open_interest(symbol)
        
        if oi_delta > 0:
            signal = "🟢 COMPRADO"
            bias = "📈 VIÉS DE ALTA"
        elif oi_delta < 0:
            signal = "🔴 VENDIDO"
            bias = "📉 VIÉS DE BAIXA"
        else:
            signal = "⚪ NEUTRO"
            bias = "⏳ AGUARDANDO FLUXO"
            
        return {
            "price": round(price, 2),
            "oi_delta": round(oi_delta, 2),
            "institutional_signal": signal,
            "market_bias": bias
        }
    except Exception as e:
        return {
            "price": 0,
            "oi_delta": 0,
            "institutional_signal": "ERRO",
            "market_bias": f"Erro: {str(e)}"
        }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    data = institutional_signal()
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@app.get("/radar")
def radar():
    return institutional_signal()
