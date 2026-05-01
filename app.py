import streamlit as st
import os
import analise
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

st.set_page_config(page_title="BTC Análise PRO", layout="wide")
st_autorefresh(interval=15000, key="datarefresh")

st.markdown("""
<style>
.main {background-color: #0E1117;}
.card {
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #30363D;
    margin-bottom: 15px;
    color: white;
    height: 180px;
}
.card h3 {margin: 8px 0 4px 0; font-size: 16px; font-weight: 600;}
.card p {margin: 0; font-size: 12px; opacity: 0.7; height: 40px; overflow: hidden;}
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 8px;
}
.green {background: rgba(16, 185, 129, 0.2); color: #10B981;}
.red {background: rgba(239, 68, 68, 0.2); color: #EF4444;}
.lock {float: right; opacity: 0.4;}
</style>
""", unsafe_allow_html=True)

def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
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
    
    col1, col2 = st.columns(2)
    with col1:
        ativo = st.selectbox("Ativo", ["BTC", "ETH", "SOL", "BNB", "XRP"], index=0)
    with col2:
        timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=3)
    
    try:
        with st.spinner(f"Buscando {ativo}USDT {timeframe}..."):
            df = analise.get_data(ativo, timeframe)
            df = analise.calcular_indicadores(df)
            preco_atual = analise.get_preco(ativo)
        
        st.subheader(f"{ativo}USDT • {timeframe}")
        st.metric("Preço Atual", f"${preco_atual:,.2f}")
        
        fig = go.Figure(data=[go.Candlestick(
            x=df['timestamp'], open=df['open'], high=df['high'], low=df['low'], close=df['close'],
            increasing_line_color='#10B981', decreasing_line_color='#EF4444'
        )])
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        ultimo = df.iloc[-1]
        rsi = float(ultimo['rsi']) if not pd.isna(ultimo['rsi']) else 50.0
        macd = float(ultimo['macd']) if not pd.isna(ultimo['macd']) else 0.0
        score = 50
        if rsi < 30: score += 20
        elif rsi > 70: score -= 20
        if macd > 0: score += 15
        else: score -= 15
        score = max(0, min(100, int(score)))
        
        sinal = "COMPRA" if score > 60 else "VENDA" if score < 40 else "NEUTRO"
        cor_sinal = "green" if sinal == "COMPRA" else "red" if sinal == "VENDA" else "#8B949E"
        
        st.markdown(f"""
        <div class="card" style="background: #161B22; height:auto; text-align:center;">
            <h3 style="margin:0; color:{cor_sinal};">SINAL: {sinal}</h3>
            <p style="margin:5px 0; color:#8B949E;">Score: {score}/100 | RSI: {rsi:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        def safe_float(val, default=0.0):
            try:
                return float(val.item()) if hasattr(val, 'item') else float(val)
            except:
                return default
        
        def safe_suporte_resistencia():
            try:
                suporte = df['low'].rolling(20).min().iloc
