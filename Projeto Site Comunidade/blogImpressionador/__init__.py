from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a4eaac0a59dee3e7c21d916ddb3caaf1'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blog.db'

database = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
login_manager.login_view = "login"
login_manager.login_message = "Faça o login para acessar"
login_manager.login_message_category = "alert-info"

from blogImpressionador import routes
