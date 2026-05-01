import streamlit as st
import pandas as pd
import analise

st.set_page_config(page_title="BTC Probabilidade", layout="wide")

if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("BTC Dashboard - Login")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if user == "admin" and senha == "1234":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    st.stop()

st.title("BTC • ANÁLISE EM TEMPO REAL")
st.caption("Atualiza a cada 1 min")

df = pd.DataFrame({'close': [78247, 78300, 78200, 78150]})
resultado = analise.calcular_probabilidade(df)

col1, col2, col3 = st.columns(3)
col1.metric("Probabilidade ALTA", f"{resultado['prob_alta']}%")
col2.metric("Probabilidade BAIXA", f"{resultado['prob_baixa']}%")
col3.metric("Score", f"{resultado['score']}/100")

st.progress(resultado['prob_alta'] / 100)
st.write(f"**Potencial de movimento:** ~5.0% { 'ALTA' if resultado['prob_alta'] > 50 else 'BAIXA' }")
st.write(f"**Alvo projetado:** ${resultado['alvo']:,.0f}")
