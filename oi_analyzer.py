from binance_api import get_price, get_open_interest

def institutional_signal():

    price = get_price()
    oi_change = get_open_interest()

    if oi_change > 0:
        direction = "🟢 Institucional entrando COMPRADO"
    elif oi_change < 0:
        direction = "🔴 Institucional entrando VENDIDO"
    else:
        direction = "⚪ Sem fluxo institucional"

    return {
        "price": price,
        "oi_delta": oi_change,
        "signal": direction
    }
