import streamlit as st
import os
import pandas as pd
import analise

st.set_page_config(page_title="BTC Análise", layout="wide")

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
.score {font-size: 48px; font-weight: bold;}
.label {color: #8B949E; font-size: 14px;}
</style>
""", unsafe_allow_html=True)

# LOGIN
def login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        usuario_correto = os.environ.get("USER", "admin")
        senha_correta = os.environ.get("PASS", "123456")

        if st.button("Entrar"):
            if usuario == usuario_correto and senha == senha_correta:
                st.success("Login realizado com sucesso!")
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    # DASHBOARD
    st.title("BTC Análise Dashboard")
    resultado = analise.calcular_probabilidade(None)
    st.metric("Score", resultado['score'])
    st.metric("Prob. Alta", f"{resultado['prob_alta']}%")
    st.metric("Prob. Baixa", f"{resultado['prob_baixa']}%")
