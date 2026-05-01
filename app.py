import streamlit as st
import os
import analise
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="BTC Análise PRO", layout="wide")
st_autorefresh(interval=15000, key="datarefresh")
st.markdown("<style>.main{background-color:#0E1117;}</style>", unsafe_allow_html=True)

def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>Login</h1>", unsafe_allow_html=True)
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario == os.environ.get("USER", "admin") and senha == os.environ.get("PASS", "123456"):
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    st.title("BTC Análise PRO - Dados Reais")
    ativo = st.selectbox("Ativo", ["BTC", "ETH", "SOL", "BNB", "XRP"], index=0)
    timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=3)
    
    try:
        df = analise.get_data(ativo, timeframe)
        df = analise.calcular_indicadores(df)
        preco_atual = analise.get_preco(ativo)
        
        st.metric("Preço Atual", f"${preco_atual:,.2f}")
        fig = go.Figure(data=[go.Candlestick(x=df['timestamp'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])])
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        ultimo = df.iloc[-1]
        rsi = float(ultimo['rsi'].item()) if pd.notna(ultimo['rsi']) else 50.0
        macd = float(ultimo['macd'].item()) if pd.notna(ultimo['macd']) else 0.0
        
    except Exception as e:
        st.error(f"Erro: {e}")
