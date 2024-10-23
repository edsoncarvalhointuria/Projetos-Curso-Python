import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.filedialog import askopenfilename
import xmltodict
import requests
import pandas as pd

requisicao = requests.get('https://economia.awesomeapi.com.br/xml/available/uniq')
dict_moedas = xmltodict.parse(requisicao.text)['xml']

lista_moedas = list(dict_moedas.keys())


def pegar_cotacao():
    text_data = str(data.get_date()).replace('-', '')
    text_moeda = dropdown.get().upper()
    requisicao = requests.get(f'https://economia.awesomeapi.com.br/{text_moeda}-BRL/?start_date={text_data}&end_date={text_data}')
    if text_moeda and '404' not in requisicao.text:
        cotacao = requisicao.json()[0]
        label_cotacao['text'] = f'A cotação do {dict_moedas[text_moeda]} no dia {data.get()} foi de: R${cotacao['bid']}'
    else:
        label_cotacao['text'] = 'Cotação não encontrada'


def escolher_arquivo():
    var_caminho.set(askopenfilename(title='Selecione o Arquivo com as moedas'))
    if var_caminho.get():
        label_arquivo['text'] = f'Arquivo Selecionado: {var_caminho.get()}'



def atualizar_cotacoes():
    label_status['text'] = 'Gerando Arquivo'
    try:
        text_data_inicial = data_inicial.get_date()
        text_data_final = data_final.get_date()
        df_moedas = pd.read_excel(var_caminho.get())
        df_resultado = pd.DataFrame()
        for moeda in df_moedas.iloc[:, 0]:
            link = f'https://economia.awesomeapi.com.br/{moeda.upper()}-BRL/{int((text_data_final-text_data_inicial).days)}?start_date={str(text_data_inicial).replace('-', '')}&end_date={str(text_data_final).replace('-', '')}'
            requisicao = requests.get(link)
            cotacoes = requisicao.json()
            if requisicao.status_code == 200:
                df_resultado[moeda.upper()] = [cotacao.get('bid') for cotacao in cotacoes]
            else:
                df_resultado = pd.concat([df_resultado, pd.DataFrame({moeda.upper():['Não Encontrado']})], axis=1)
        df_resultado.to_excel('Resultado.xlsx')
        label_status['text'] = 'Arquivo Finalizado'
    except:
        label_status['text'] = 'Arquivo com formato invalido'

janela = tk.Tk()
janela.title('Cotações')
janela.columnconfigure([0,1,2], weight=1)

label = tk.Label(text='Cotação Moeda Específica', borderwidth=2, relief='solid')
label.grid(row=0, column=0, columnspan=3, sticky='NEWS', padx=10, pady=10)

label = tk.Label(text='Escolha a moeda que deseja consultar:', anchor='e')
label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='NEWS')
dropdown= ttk.Combobox(janela, values=lista_moedas)
dropdown.grid(row=1, column=2, padx=10, pady=10, sticky='NEWS')

label = tk.Label(text='Escolha uma data para consulta: ', anchor='e')
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='NEWS')
data = DateEntry(year=2024, locale='pt_br')
data.grid(row=2, column=2, padx=10, pady=10, sticky="NEWS")

label_cotacao = tk.Label(text='')
label_cotacao.grid(row=3, column=0, padx=10, pady=10, sticky='NEWS', columnspan=2)

button = tk.Button(text='Pegar Cotação', command=pegar_cotacao)
button.grid(row=3, column=2, padx=10, pady=10, sticky="NEWS")

### segunda parte

label = tk.Label(text='Cotação Múltiplas Moedas', borderwidth=2, relief='solid')
label.grid(row=4, column=0, sticky='NEWS', columnspan=3, padx=10, pady=10)

label_arquivo = tk.Label(text='Nenhum Arquivo Selecionado', anchor='e')
label_arquivo.grid(row=6, column=0, columnspan=3, sticky='NEWS', padx=10, pady=10)
    
var_caminho = tk.StringVar()

label = tk.Label(text='Selecione um arquivo em Excel com as Moedas na Coluna A: ')
label.grid(row=5, column=0, columnspan=2, sticky='NEWS', padx=10, pady=10)
button = tk.Button(text='Escolher Arquivo', command=escolher_arquivo)
button.grid(row=5, column=2, padx=10, pady=10, sticky='NEWS')

label = tk.Label(text='Escolha a Data Inicial: ', anchor='e')
label.grid(row=7, column=0, padx=10, pady=10, sticky='NEWS')
data_inicial = DateEntry(year=2024, locale='pt_br')
data_inicial.grid(row=7, column=1, padx=10, pady=10, sticky='NEWS')

label = tk.Label(text='Escolha a Data Final: ', anchor='e')
label.grid(row=8, column=0, padx=10, pady=10, sticky='NEWS')
data_final = DateEntry(year=2024,  locale='pt_br')
data_final.grid(row=8, column=1, padx=10, pady=10, sticky='NEWS')

label_status = tk.Label(text='')
label_status.grid(row=9, column=1, columnspan=2, padx=10, pady=10, sticky='NEWS')


button = tk.Button(text='Clique aqui para atualizar as cotações', command=atualizar_cotacoes)
button.grid(row=9, column=0, padx=10, pady=10, sticky='NEWS')

button = tk.Button(text='Fechar', command=janela.destroy)
button.grid(row=10, column=2, padx=10, pady=10, sticky='NEWS')






janela.mainloop()