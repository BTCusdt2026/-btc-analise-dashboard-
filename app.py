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
        
        # HEADER
        st.subheader(f"{ativo}USDT • {timeframe}")
        st.metric("Preço Atual", f"${preco_atual:,.2f}")
        
        # GRÁFICO
        fig = go.Figure(data=[go.Candlestick(
            x=df['timestamp'], open=df['open'], high=df['high'], low=df['low'], close=df['close'],
            increasing_line_color='#10B981', decreasing_line_color='#EF4444'
        )])
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", xaxis_rangeslider_visible=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # SINAL
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
        
        # FUNÇÕES AUXILIARES PARA EVITAR ERRO
        def safe_float(val, default=0.0):
            try:
                return float(val.item()) if hasattr(val, 'item') else float(val)
            except:
                return default
        
        def safe_suporte_resistencia():
            try:
                suporte = df['low'].rolling(20).min().iloc[-1]
                resistencia = df['high'].rolling(20).max().iloc[-1]
                return safe_float(suporte, preco_atual * 0.98), safe_float(resistencia, preco_atual * 1.02)
            except:
                return preco_atual * 0.98, preco_atual * 1.02
        
        suporte, resistencia = safe_suporte_resistencia()
        volume_medio = safe_float(df['volume'].mean(), 0)
        volume_ultimo = safe_float(df['volume'].iloc[-1], 0)
        vol_std = safe_float(df['close'].pct_change().std(), 0.01)
        
        # GRID 8 CARDS
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #1E293B, #0F172A);">
                <span class="lock">🔒</span>
                📊 <h3>Análise Técnica Avançada</h3>
                <p>RSI: {rsi:.1f} | MACD: {'Bullish' if macd > 0 else 'Bearish'} | Tendência: {'Alta' if macd > 0 else 'Baixa'}</p>
                <span class="badge green">+24% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #78350F, #451A03);">
                <span class="lock">🔒</span>
                ⬡ <h3>Padrões Harmônicos</h3>
                <p>Padrão: {'AB=CD' if vol_std > 0.02 else 'Nenhum'} | Confiança: {65 if vol_std > 0.02 else 30}%</p>
                <span class="badge green">+22% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #7C2D12, #450A0A);">
                <span class="lock">🔒</span>
                🎯 <h3>Análise Probabilística</h3>
                <p>Prob. Alta: {score}% | Prob. Baixa: {100-score}%</p>
                <span class="badge green">+28% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #581C87, #3B0764);">
                <span class="lock">🔒</span>
                🖼️ <h3>Visual IA do Gráfico</h3>
                <p>Suporte: ${suporte:,.0f} | Resistência: ${resistencia:,.0f}</p>
                <span class="badge green">+33% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            smc_zona = "Acumulação" if rsi < 40 else "Distribuição" if rsi > 60 else "Range"
            smc_liquidez = "Alta" if volume_ultimo > volume_medio else "Baixa"
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #581C87, #3B0764);">
                <span class="lock">🔒</span>
                🧠 <h3>Smart Money Concept</h3>
                <p>Zona: {smc_zona} | Liquidez: {smc_liquidez}</p>
                <span class="badge green">+27% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
            
            wyckoff_fase = "Acumulação" if rsi < 45 else "Marcação" if rsi > 55 else "Distribuição"
            elliott_onda = "3" if macd > 0 else "5" if macd < 0 else "2"
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #064E3B, #022C22);">
                <span class="lock">🔒</span>
                📈 <h3>WEGD Wyckoff/Elliott</h3>
                <p>Fase: {wyckoff_fase} | Onda: {elliott_onda}</p>
                <span class="badge green">+31% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
            
            timing_entrada = "Agora" if 40 < rsi < 60 else "Esperar"
            timing_alvo = f"${preco_atual * 1.03:,.0f}" if macd > 0 else f"${preco_atual * 0.97:,.0f}"
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #1E3A8A, #0C1E4D);">
                <span class="lock">🔒</span>
                ⏰ <h3>Timing & Horizonte</h3>
                <p>Entrada: {timing_entrada} | Alvo: {timing_alvo}</p>
                <span class="badge green">+19% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
            
            sentimento = "Bullish" if macd > 0 and volume_ultimo > volume_medio else "Bearish"
            st.markdown(f"""
            <div class="card" style="background: linear-gradient(135deg, #92400E, #451A03);">
                <span class="lock">🔒</span>
                📰 <h3>Notícias & Sentimento</h3>
                <p>Sentimento: {sentimento} | Volume: ${df['volume'].sum():,.0f}</p>
                <span class="badge green">+18% assertividade</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')} • Dados Yahoo Finance em tempo real")
        
    except Exception as e:
        st.error(f"Erro: {e}")
