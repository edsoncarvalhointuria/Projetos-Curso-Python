# Onde vamos fazer a estrutura do banco de dados
from datetime import datetime, timezone
from fakepinterest import database, login_manager, bcrypt
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String, nullable = False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)


class Foto(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True)
    data = database.Column(database.DateTime, nullable = False, default=datetime.now(timezone.utc))
    imagem = database.Column(database.String, default="default.png")
    id_usuario = database.Column(database.Integer, database.ForeignKey("usuario.id"), nullable=False)


