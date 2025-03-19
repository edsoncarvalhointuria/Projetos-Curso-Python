from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path


db = create_engine(f'sqlite:///{Path(Path(__file__).absolute().parent.parent, "database/meubanco.db")}') # CRIANDO O BANCO DE DADOS, DEPOIS ADICIONAR O LINK
Sessao = sessionmaker(bind=db) #CRIANDO UMA SESSÃO (BASICAMENTE UM SESSÃO NESTE BANCO DE DADOS)
session = Sessao() # SOMENTE UMA CONVENSÃO

Base = declarative_base() #CRIA UMA CLASSE BASE PARA TRANSFORMAR SUAS SUBCLASSES EM TABELAS

class Usuario(Base):
    __tablename__= "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    first_name = Column("primeiro nome", String)
    last_name = Column("ultimo nome", String)
    email = Column("email", String, unique=True)
    password = Column("senha", String)
    admin = Column("admin", Boolean)

    def __init__(self, first_name, last_name, email, password, admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.admin = admin


Base.metadata.create_all(bind=db)

    

