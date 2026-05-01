import streamlit as st
import os
import analise
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="BTC Análise PRO", layout="wide")
st_autorefresh(interval=10000, key="datarefresh") # Atualiza a cada 10s

st.markdown("""
<style>
.main {background-color: #0E1117;}
.card {
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #30363D;
    margin-bottom: 15px;
    color: white;
}
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
    
    # SELETORES
    col1, col2 = st.columns(2)
    with col1:
        ativo = st.selectbox("Ativo", ["BTC", "ETH", "SOL", "BNB", "XRP"], index=0)
    with col2:
        timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=3)
    
    # BUSCA DADOS REAIS
    try:
        with st.spinner(f"Buscando {ativo}USDT {timeframe} da Binance..."):
            df = analise.get_data(ativo, timeframe)
            df = analise.calcular_indicadores(df)
            preco_atual = analise.get_preco(ativo)
        
        # HEADER COM PREÇO REAL
        col1, col2 = st.columns([3,1])
        with col1:
            st.subheader(f"{ativo}USDT • {timeframe}")
        with col2:
            var_24h = ((df['close'].iloc[-1] - df['close'].iloc[-96]) / df['close'].iloc[-96]) * 100
            cor = "green" if var_24h >= 0 else "red"
            st.markdown(f"<h2 style='text-align:right;'>${preco_atual:,.2f}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:right; color:{cor};'>{var_24h:+.2f}% 24h</p>", unsafe_allow_html=True)
        
        # GRÁFICO CANDLESTICK REAL
        fig = go.Figure(data=[go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            increasing_line_color='#10B981',
            decreasing_line_color='#EF4444'
        )])
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            xaxis_rangeslider_visible=False,
            height=500,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # INDICADORES REAIS
        ultimo = df.iloc[-1]
        rsi = ultimo['rsi']
        macd = ultimo['macd']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("RSI 14", f"{rsi:.1f}", "Sobrecomprado" if rsi > 70 else "Sobrevendido" if rsi < 30 else "Neutro")
        col2.metric("MACD", "Bullish" if macd > 0 else "Bearish")
        col3.metric("Volume", f"${df['volume'].iloc[-1]:,.0f}")
        
        st.caption(f"Dados em tempo real da Binance • Última atualização: {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        st.error(f"Erro ao buscar dados da Binance: {e}")
        st.info("Se o erro persistir, Railway pode ter IP bloqueado. A gente troca pra CoinGecko.")
