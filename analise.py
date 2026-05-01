import pandas as pd
import numpy as np

def calcular_probabilidade(df):
    if df is None or len(df) < 50:
        return {'prob_alta': 50, 'prob_baixa': 50, 'score': 0, 'alvo': 0, 'posicao_range': 0.5}
    
    df = df.copy()
    preco_atual = df['close'].iloc[-1]
    
    # MÓDULO 1: Range 20 períodos
    topo = df['close'].rolling(20).max().iloc[-1]
    fundo = df['close'].rolling(20).min().iloc[-1]
    posicao = (preco_atual - fundo) / (topo - fundo + 0.0001)
    
    score_total = 0
    pesos = 0
    
    # MÓDULO 2: RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / (loss + 0.0001)
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    if rsi < 30: score_total += 15; pesos += 1  # Sobre venda = alta
    elif rsi > 70: score_total -= 15; pesos += 1  # Sobre compra = baixa
    
    # MÓDULO 3: MACD
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()
    if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] < signal.iloc[-2]:
        score_total += 20; pesos += 1  # Cruzamento alta
    elif macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] > signal.iloc[-2]:
        score_total -= 20; pesos += 1  # Cruzamento baixa
    
    # MÓDULO 4: Volume Spike
    vol_media = df['volume'].rolling(20).mean().iloc[-1]
    vol_atual = df['volume'].iloc[-1]
    if vol_atual > vol_media * 1.5:
        if df['close'].iloc[-1] > df['open'].iloc[-1]: score_total += 25; pesos += 1
        else: score_total -= 25; pesos += 1
    
    # MÓDULO 5: Média Móvel 200
    ema200 = df['close'].ewm(span=200).mean().iloc[-1]
    if preco_atual > ema200: score_total += 10; pesos += 1
    else: score_total -= 10; pesos += 1
    
    # MÓDULO 6: Candle Pattern
    o, h, l, c = df['open'].iloc[-1], df['high'].iloc[-1], df['low'].iloc[-1], df['close'].iloc[-1]
    corpo = abs(c - o)
    sombra_sup = h - max(o, c)
    sombra_inf = min(o, c) - l
    if corpo > 0 and sombra_inf > corpo * 2 and sombra_sup < corpo * 0.5:
        score_total += 15; pesos += 1  # Martelo = alta
    elif corpo > 0 and sombra_sup > corpo * 2 and sombra_inf < corpo * 0.5:
        score_total -= 15; pesos += 1  # Estrela cadente = baixa
    
    # MÓDULO 7: Suporte/Resistência
    dist_suporte = abs(preco_atual - fundo) / preco_atual
    dist_resist = abs(topo - preco_atual) / preco_atual
    if dist_suporte < 0.01: score_total += 12; pesos += 1  # Perto suporte
    if dist_resist < 0.01: score_total -= 12; pesos += 1  # Perto resistência
    
    # MÓDULO 8: Tendência Curta
    ema5 = df['close'].ewm(span=5).mean().iloc[-1]
    ema10 = df['close'].ewm(span=10).mean().iloc[-1]
    if ema5 > ema10: score_total += 8; pesos += 1
    else: score_total -= 8; pesos += 1
    
    # Cálculo final da probabilidade
    if pesos == 0: pesos = 1
    score_final = score_total / pesos
    prob_alta = 50 + score_final
    prob_alta = max(5, min(95, prob_alta))
    prob_baixa = 100 - prob_alta
    
    # Alvo baseado na direção
    if prob_alta > 55: alvo = preco_atual * 1.05
    elif prob_baixa > 55: alvo = preco_atual * 0.95
    else: alvo = preco_atual
    
    return {
        'prob_alta': int(prob_alta),
        'prob_baixa': int(prob_baixa),
        'score': int(abs(score_final) * 2),
        'alvo': alvo,
        'posicao_range': posicao,
        'rsi': int(rsi) if 'rsi' in locals() else 50
    }
