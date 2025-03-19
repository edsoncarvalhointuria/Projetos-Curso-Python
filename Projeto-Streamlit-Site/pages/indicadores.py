import streamlit as st
from data_loader import carregar_base
from unidecode import unidecode

df = carregar_base()


def criar_card(icon, number, text, column):
    container = column.container(border=True, )
    coluna_esquerda, coluna_direita = container.columns([1,2.5])
    coluna_esquerda.image(f"imagens/indicadores/{icon}")
    coluna_direita.write(str(number))
    coluna_direita.write(text)

proj_fechados = df[df["Status"].isin(["Finalizado", "Em andamento"])]
colunas = st.columns([2,2,2])

criar_card(icon="oportunidades.png", column=colunas[0], number=df['Status'].count(), text="Oportunidades")
criar_card(icon="projetos_fechados.png", column=colunas[1], number=proj_fechados["Status"].count(), text="Projetos Fechados")
criar_card(icon="em_andamento.png", column=colunas[2], number=proj_fechados.loc[proj_fechados['Status']=="Em andamento", "Status"].count(), text="Em Andamento")


criar_card(icon="total_orcado.png", column=colunas[0], number=f"R${proj_fechados['Valor Orçado'].sum():,}", text="Total Orçado")
criar_card(icon="total_pago.png", column=colunas[1], number=f"R${proj_fechados['Valor Negociado'].sum():,}", text="Total Pago")
criar_card(icon="desconto.png", column=colunas[2], number=f"R${proj_fechados['Desconto Concedido'].sum():,}", text="Desconto")

import plotly.express as px

status_df = data=df["Status"].value_counts(sort=True).reset_index().rename(columns={"count":"Quantidade"})
funil = px.funnel(data_frame=status_df, x="Quantidade", y="Status")
st.plotly_chart(funil)

# icones = Path(Path(__file__).parent.parent, "imagens/indicadores")
# coluna = 0
# for card in cards:
#     for i, icone in enumerate(icones.iterdir()):
#         if unidecode(card.lower()) in icone.name.replace("_", " "):
#             criar_card(icon=str(icone), column=colunas[coluna], number=cards[card], text=card)
#             coluna+=1
#             if coluna > 2:
#                 coluna=0
#             break

        

        
