from pathlib import Path
import sys

BASE_DIR = Path(__file__).absolute().parent
sys.path.append(BASE_DIR)


import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from functools import partial
from pages.models import session, Usuario

st.markdown(f'Veja Aqui: {BASE_DIR}')


# DESSE JEITO TAMBÉM FUNCIONA
# credentials = {'usernames':{
#     'edson@gmail.com':{'name':"Edson Carvalho Inturia", 'password': '321321'},
#     'teste@gmail.com':{'name':"Testando", 'password': '123123'},
# }}
# print(stauth.Hasher.hash_passwords(credentials))

with open('./.streamlit/config.YAML') as arquivo:
    config = yaml.load(arquivo, SafeLoader)
    # credentials = config["credentials"]


def pegar_usuarios():
    return session.query(Usuario).all()

lista_usuarios = pegar_usuarios()
credentials = {"usernames":{
    usuario.email:{"first_name":usuario.first_name,"last_name":usuario.last_name, "email":usuario.email, "password":usuario.password, "admin":usuario.admin} for usuario in lista_usuarios
}}


authenticator = stauth.Authenticate(credentials, cookie_name=config['cookie']['name'],cookie_key=config['cookie']['key'],cookie_expiry_days=config['cookie']['expiry_days'])


def autenticar_usuario(authenticator):
    authenticator.login()
    auth_status = st.session_state.get('authentication_status')
    name = st.session_state.get('name')
    username = st.session_state.get('username')
    if auth_status:
        # st.switch_page(page='homepage.py')
        return name, username
    elif auth_status == False:
        st.error("Usuário ou Senha Invalidos", icon="🚨")
    else:
        (st.error("Preencha o formulário para fazer login", icon="⚠"))

def logout(authenticator):
    with st.sidebar:
        teste = authenticator.logout()
    

dados_login = autenticar_usuario(authenticator)

if dados_login:
    
    is_admin = credentials["usernames"][dados_login[1]]["admin"]
    if is_admin:
        nav = st.navigation({
            "Home":[st.Page("pages/homepage.py",title="EdSpace")], 
            "Dashboards":[st.Page("pages/dashboard.py", title="Dashboard"), st.Page("pages/indicadores.py", title="Indicadores")], 
            "Conta":[st.Page("pages/criar_conta.py", title="Criar Conta"), st.Page(partial(logout,authenticator), title="Sair"),]
        })
    else:
        nav = st.navigation({
            "Home":[st.Page("pages/homepage.py",title="Edspace")], 
            "Dashboards":[st.Page("pages/dashboard.py", title="Dashboard"), st.Page("pages/indicadores.py", title="Indicadores")], 
            "Conta":[st.Page(partial(logout,authenticator), title="Sair"),]
        })
    
    nav.run()
else:
        nav = st.navigation({"Conta":[st.Page(partial(logout,authenticator), title="Sair"),]})


