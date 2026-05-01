import streamlit as st
import pandas as pd
import analise

st.set_page_config(page_title="BTC Análise PRO", layout="wide", page_icon="📊")

# CSS Dark PRO
st.markdown("""
<style>
    .main {background-color: #0E1117;}
    .card {
        background-color: #161B22; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #30363D;
        margin-bottom: 15px;
    }
    .score {font-size: 48px; font-weight: bold; color: #58A6FF;}
    .label {color: #8B949E; font-size: 14px;}
</style>
""", unsafe_allow_html=True)

# LOGIN
def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>BTC Análise PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#8B949E;'>Análise em tempo real com 8 módulos de IA</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if usuario == st.secrets["USER"] and senha == st.secrets["PASS"]:
                    st.session_state["logado"] = True
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("<p style='text-align:center; color:#8B949E; font-size:12px;'>Powered by SMC + WEGD + Visual IA + Harmônicos</p>", unsafe_allow_html=True)

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
    st.stop()

# ===== DASHBOARD =====
st.title("BTC • ANÁLISE EM TEMPO REAL")
st.caption("Atualiza a cada 1 min • Confluência de 8 módulos PRO")

# Puxa dados do analise.py
try:
    score_total = analise.calcular_score_total()
    prob_alta, prob_baixa = analise.calcular_probabilidade()
    alvo, potencial = analise.calcular_alvo()
except:
    score_total, prob_alta, prob_baixa, alvo, potencial = 0, 50, 50, 0, 0

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="label">PROBABILIDADE</p>', unsafe_allow_html=True)
    st.markdown(f'<span style="color:#3FB950;">ALTA: {prob_alta}%</span> / <span style="color:#F85149;">BAIXA: {prob_baixa}%</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="label">SCORE DE CONFLUÊNCIA</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="score">{score_total}/100</p>', unsafe_allow_html=True)
    st.progress(score_total)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="label">ALVO PROJETADO</p>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color:#F85149;">${alvo:,.2f}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="label">Potencial: ~{potencial}% BAIXA</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### Diagnóstico PRO")
with st.expander("Ver peso de cada módulo"):
    st.write("**Visual IA do Gráfico:** 0/33")
    st.write("**WEGD Wyckoff/Elliott/Gann:** 0/31") 
    st.write("**Smart Money Concepts:** 0/27")
    st.write("**Análise Probabilística:** 0/28")
    st.write(f"**Total:** {score_total}/100")

st.button("Sair", on_click=lambda: st.session_state.update({"logado": False}))
