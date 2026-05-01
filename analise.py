import pandas as pd
import random

def calcular_probabilidade(df):
    """
    Se df for None, retorna valores fake pra testar o dashboard.
    Quando você tiver dados reais, troca essa lógica aqui.
    """
    if df is None:
        # Dados de teste pra mostrar no dashboard
        score = random.randint(40, 95)
        prob_alta = random.randint(30, 80)
        prob_baixa = 100 - prob_alta
        return {
            "score": score,
            "prob_alta": prob_alta,
            "prob_baixa": prob_baixa
        }
    
    # Aqui vai sua lógica real quando tiver o df
    # Exemplo:
    # score = df['close'].pct_change().mean() * 100
    # return {"score": int(score), "prob_alta": 60, "prob_baixa": 40}
    
    return {"score": 50, "prob_alta": 50, "prob_baixa": 50}
