import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import timedelta
from pathlib import Path


@st.cache_data
def pegar_acoes(empresas):
    empresas = " ".join(empresas)
    ticker = yf.Tickers(empresas)#Tickers para varios, Ticker para um
    acoes = ticker.history(period='1d', start='2010-01-01', end='2024-10-17')#no period eu coloco se eu quero mensal, diario ou anual
    
    return acoes['Close']

def carregar_indices():
    caminho = Path("Projeto-Streamlit-Acoes", "IBOV.csv")
    if caminho.exists():
        lista_empresas = pd.read_csv(str(caminho.absolute()).replace("\\", "/"), sep=";", encoding="latin-1")["Código"] + ".SA"
    else:
        lista_empresas = pd.read_csv("IBOV.csv", sep=";", encoding="latin-1")["Código"] + ".SA"
    return list(lista_empresas.dropna(how="all"))


#PEGANDO DADOS
lista_empresas = carregar_indices()
acoes = pegar_acoes(lista_empresas)

st.write("""# App Preços de Ações
O gráfico abaixo representa o preço das ações ao longo dos anos:""")

st.sidebar.header("Filtros")# TUDO QUE EU QUERO QUE APAREÇA NO SIDE BAR, EU TENHO QUE COLOCAR .SIDEBAR EX ABAIXO

#FILTROS
filtro_select = st.sidebar.multiselect("Escolha As Empresas", acoes.columns)#MULTISELECT
if filtro_select:
    acoes = acoes[filtro_select]
    if len(filtro_select)==1:
        acoes = acoes.rename(columns={filtro_select[0]:filtro_select[0].replace(".SA", "")})#SE O NOME DA COLUNA TIVER PONTO. ELE NÂO CONSEGUE

data_final = acoes.index.to_pydatetime().max()
data_inicial = acoes.index.to_pydatetime().min()
periodo = st.sidebar.slider("Selecione o período", data_final, data_inicial, value=(data_final - timedelta(weeks=200), data_final), step=timedelta(days=1))

if periodo:
    acoes = acoes.loc[periodo[0]:periodo[1]]




st.line_chart(data=acoes)



def definir_ativo(ativo, resultado):
    if resultado < 0:
        performance = f"  \n{ativo}: :red[{resultado:.2%}]"
    elif resultado > 0:
        performance = f"  \n{ativo}: :green[{resultado:.2%}]"
    else:
        performance = f"  \n{ativo}: {resultado:.2%}"
    return performance

carteira = [1000 for ativo in acoes]#DEFININDO UMA CARTEIRA FICTICIA
valor_inicial_carteira = sum(carteira)
performance_ativos = ""
for i, ativo in enumerate(acoes):
    try:
        resultado_ativo=float(acoes.iloc[-1, i]/acoes.iloc[0,i]-1)
        if not pd.isna(resultado_ativo):
            carteira[i] *= (resultado_ativo+1.0)
        performance_ativos+= definir_ativo(ativo, resultado_ativo)
    except IndexError:
        pass

valor_final_carteira = sum(carteira)
perfomance_carteira = valor_final_carteira/valor_inicial_carteira - 1
performance_ativos += definir_ativo(" \nPerformance da carteira com todos ativos", perfomance_carteira)

st.write(f"""
### Performance dos ativos:
Essa foi a performance de cada ativo no período selecionado:
         
{performance_ativos}""")
