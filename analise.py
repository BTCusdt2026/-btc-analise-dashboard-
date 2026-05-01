import pandas as pd

def calcular_probabilidade(df):
    preco_atual = df['close'].iloc[-1]
    topo = df['close'].rolling(20).max().iloc[-1]
    fundo = df['close'].rolling(20).min().iloc[-1]
    
    if pd.isna(topo) or pd.isna(fundo):
        topo, fundo = preco_atual * 1.05, preco_atual * 0.95
    
    posicao = (preco_atual - fundo) / (topo - fundo + 0.0001)
    
    if posicao < 0.1:
        prob_alta, prob_baixa = 62, 38
        alvo = preco_atual * 1.05
    elif posicao > 0.9:
        prob_alta, prob_baixa = 28, 72
        alvo = preco_atual * 0.942
    else:
        prob_alta, prob_baixa = 50, 50
        alvo = preco_atual
    
    score = abs(prob_alta - 50) * 2
    
    return {
        'prob_alta': prob_alta,
        'prob_baixa': prob_baixa,
        'score': int(score),
        'alvo': alvo,
        'posicao_range': posicao
    }
