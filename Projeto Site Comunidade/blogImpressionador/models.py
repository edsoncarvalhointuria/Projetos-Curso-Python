from blogImpressionador import database, login_manager
from datetime import datetime
from datetime import UTC
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(id_usuario)


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship("Post", backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default="Não Informado")

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default = lambda: datetime.now(UTC))
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)