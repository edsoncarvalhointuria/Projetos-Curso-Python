# from secrets import token_hex

# print(token_hex(16))

from pages.models import Usuario, session
import streamlit_authenticator as stauth

# senha_criptografada = stauth.Hasher.hash("123123")

# admin = Usuario(admin=True, email='edson@gmail.com', first_name="Edson", last_name="Carvalho Inturia", password=senha_criptografada)

# session.add(admin)
# session.commit()

users = session.query(Usuario).filter_by(password="123123").all()
for user in users:
    session.delete(user)
session.commit()
