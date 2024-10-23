#Esse arquivo não é necessário, eu fiz ele apenas para controlar melhor a criação do banco de dados
from fakepinterest import database, app
from fakepinterest.models import Usuario, Foto

with app.app_context():#O Flask exige que a criação do banco seja feita dentro de um Contexto
    database.create_all() #Cria o Banco de Dados Vazio
#DETALHE AS TABELAS SÃO CRIADAS NO ARQUIVO MODELS E DEPOIS SÃO IMPORTADAS