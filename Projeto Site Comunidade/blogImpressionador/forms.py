from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError
from blogImpressionador.models import Usuario
from flask_login import current_user


mi,ma = (6,20)

class FormFazerLogin(FlaskForm):
    email = StringField("E-mail", validators=[Email("E-mail Invalido"), DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(mi,ma)])
    lembrar_acesso = BooleanField("Lembrar do Acesso")
    botao_login = SubmitField("Login")


class FormCriarConta(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[Email("E-mail Invalido"), DataRequired()])
    senha = PasswordField("Senha", validators=[Length(mi,ma), DataRequired()])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo('senha', "As senhas estão diferentes")])
    botao_cadastrar = SubmitField("Cadastrar")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado")
        

class FormEditarPerfil(FlaskForm):
    username = StringField("Username", validators=[ DataRequired()])
    email = StringField("E-mail", validators=[Email("E-mail Invalido"), DataRequired()])
    enviar_foto = FileField("Alterar Foto", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    curso_excel = BooleanField("Excel")
    curso_powerbi = BooleanField("Power BI")
    curso_python = BooleanField("Python")
    curso_vba = BooleanField("VBA")

    botao_editar = SubmitField("Editar Perfil")

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("Já existe um usuário com este e-mail")
            

class FormCriarPost(FlaskForm):
    titulo = StringField("Titulo do Post", validators=[DataRequired(), Length(2,20)])
    corpo = TextAreaField("Mensagem", validators=[DataRequired()])
    botao_postar = SubmitField("Postar")

# csrf_token