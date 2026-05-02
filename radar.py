from oi_analyzer import institutional_signal

def radar_institucional():

    data = institutional_signal()

    signal = data["signal"]
    price = data["price"]

    if "COMPRADO" in signal:
        bias = "📈 VIÉS DE ALTA"
    elif "VENDIDO" in signal:
        bias = "📉 VIÉS DE BAIXA"
    else:
        bias = "⏳ AGUARDANDO FLUXO"

    return {
        "price": price,
        "institutional_signal": signal,
        "market_bias": bias
    }
