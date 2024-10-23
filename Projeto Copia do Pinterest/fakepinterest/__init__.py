from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__) #MEU APP
#No caso do banco de dados, temos que configurar a variável onde vai estar o banco:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db" #É bom criar um novo arquivo apenas criar o banco
#O Flask-login precisa que o nosso site esteja seguro para funcionar, nesse caso, vamos criar uma secret key
app.config["SECRET_KEY"] = "82e5fab23e9d5a7a8c4cb653a7a86e72"
app.config["UPLOAD_FOLDER"] = "static/fotos_post"
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"# Temos que passar para o gerenciador, qual a página que ele está vinculada

from fakepinterest import routes