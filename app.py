import streamlit as st
import os

st.set_page_config(page_title="BTC Análise PRO", layout="wide")

st.markdown("""
<style>
.main {background-color: #0E1117;}
</style>
""", unsafe_allow_html=True)

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
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    st.title("BTC Análise PRO")
    st.success("Login ok! Agora vamos adicionar os dados reais.")
