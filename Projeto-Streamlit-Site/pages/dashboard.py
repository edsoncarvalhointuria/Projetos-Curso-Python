import streamlit as st
import plotly.express as px
from data_loader import carregar_base

df = carregar_base()

col_esquerda, col_centro, col_direita = st.columns([1,1,1])
setor = col_esquerda.selectbox("Setor", options=list(df["Setor"].unique()))
status = col_centro.selectbox("Status", options=list(df["Status"].unique()))
with st.container(border=True):
    df = df[(df["Setor"]==setor)&(df["Status"]==status)]
    df_mes = df.groupby(by=df["Data Chegada"].dt.to_period("M")).sum(numeric_only=True).reset_index()
    df_mes["Data Chegada"] = df_mes["Data Chegada"].dt.to_timestamp()#O PLOTLY PRECISA DE UM TIMESTAMP
   
    st.write("### Total projetos por mês(R$)")
    area = px.area(df_mes, x="Data Chegada", y="Valor Negociado", )
    st.plotly_chart(area)

    col_esquerda, col_direita = st.columns([3,1])

    df_mes["Ano"] = df_mes["Data Chegada"].dt.year
    col_esquerda.write("### Comparação Orçado X Pago")
    ano = col_direita.selectbox("Ano", options=list(df_mes["Ano"].unique()))
    
    df_mes = df_mes[df_mes["Ano"]==ano]

    col_esquerda, col_direita = st.columns([1,1])
    col_esquerda.metric("Total Pago", value=f"R${df_mes['Valor Negociado'].sum():,}")
    col_direita.metric("Total Desconto", value=f"R${df_mes['Desconto Concedido'].sum():,}")

    import plotly.graph_objects as go

    barra = go.Figure(data=[
        go.Bar(name="Valor Orçamento", x=df_mes["Data Chegada"], y=df_mes["Valor Orçado"], text=df_mes["Valor Orçado"]),
        go.Bar(name="Valor Pago", x=df_mes["Data Chegada"], y=df_mes["Valor Negociado"], text=df_mes["Valor Negociado"]),
    ])
    barra.update_layout(barmode="group")
    st.plotly_chart(barra)
    