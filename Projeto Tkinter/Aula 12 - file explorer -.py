import pandas as pd
from tkinter.filedialog import askopenfilename

caminho = askopenfilename(title='Escolha o arquivo em excel')
dataframe = pd.read_excel(caminho)

print(dataframe)
