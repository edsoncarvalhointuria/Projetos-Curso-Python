# Onde são feitos os formularios
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, FileField
from wtforms.validators import EqualTo, ValidationError, Length, Email, DataRequired
from fakepinterest.models import Usuario


class UserLogin(FlaskForm):
    email = StringField("E-mail", validators= [Email(), DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Fazer Login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Email não cadastrado, crie uma conta")


class CriarConta(FlaskForm):
    email = StringField("E-mail", validators=[Email(), DataRequired()])
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,16)])
    confirmar_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Email já cadastrado, faça o login")


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao = SubmitField("Enviar Foto")