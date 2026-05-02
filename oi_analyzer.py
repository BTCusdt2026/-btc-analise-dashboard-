def institutional_flow(price_now, price_prev, oi_now, oi_prev):

    if price_now > price_prev and oi_now > oi_prev:
        return "🟢 Institucional Comprando"

    elif price_now < price_prev and oi_now > oi_prev:
        return "🔴 Institucional Vendendo"

    elif oi_now < oi_prev:
        return "⚠️ Fechamento de posições"

    return "⏳ Mercado neutro"
