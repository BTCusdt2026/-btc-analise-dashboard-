from binance_api import get_price, get_open_interest
from oi_analyzer import institutional_flow

last_price = get_price()
last_oi = get_open_interest()

def radar_signal():

    global last_price, last_oi

    price = get_price()
    oi = get_open_interest()

    signal = institutional_flow(price, last_price, oi, last_oi)

    last_price = price
    last_oi = oi

    return {
        "price": price,
        "oi": oi,
        "signal": signal
    }
