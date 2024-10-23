import streamlit as st



usuario = st.session_state.get("name").split()

coluna_esquerda, coluna_direita = st.columns([1,1])
coluna_esquerda.title("Ed🚀Space")
coluna_esquerda.write(f"#### Bem-vindo, {usuario[0]}")
botao_dashboards = coluna_esquerda.button("Dashboards Projetos")
botao_indicadores = coluna_esquerda.button("Principais Indicadores")

if botao_dashboards:
    st.switch_page("pages/dashboard.py")
elif botao_indicadores:
    st.switch_page("pages/indicadores.py")

container = coluna_direita.container(border=True)
container.image("imagens/time-comunidade.jpeg", use_column_width=True)