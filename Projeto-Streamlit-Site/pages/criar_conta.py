import streamlit as st
import streamlit_authenticator as stauth
from pages.models import session, Usuario
import re
import time

st.title("Criar Conta")

with st.form("form_criar_conta"):
    nomes = st.columns(2)
    first_name = nomes[0].text_input("Primeiro Nome")
    last_name = nomes[1].text_input("Último Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    admin = st.checkbox("Acesso Admin")
    submit = st.form_submit_button("Salvar")

if submit:
    if first_name and last_name and email and password:
        padrao = re.compile(r'.+@\w+\..+')
        if not re.findall(padrao, email):
            st.error("Email Invalido", icon="🚨")
        elif len(password) < 3:
            st.error("Senha Invalida", icon="🚨")
        else:
            query_user = session.query(Usuario).filter_by(email=email).all()
            if query_user:
                st.error("Email já cadastrado", icon="🚨")
            else:
                password = stauth.Hasher.hash(password)
                new = Usuario(admin=admin, email=email, first_name=first_name, last_name=last_name, password=password)
                session.add(new)
                session.commit()
                st.write(":green[Cadastro realizado com sucesso]")
                time.sleep(2)
                st.switch_page("pages/homepage.py")
                
    else:
        st.error("Preencha todos os campos", icon="🚀")
