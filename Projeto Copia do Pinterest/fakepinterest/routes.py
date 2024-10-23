# Onde vamos fazer as rotas
from flask import render_template, url_for, redirect
from fakepinterest import app, bcrypt, database
from fakepinterest.forms import CriarConta, UserLogin, FormFoto
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from pathlib import Path

@app.route("/", methods = ["POST", "GET"])
def homepage():
    form_userlogin = UserLogin()
    if form_userlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_userlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), form_userlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("homepage.html", form = form_userlogin)


@app.route("/criarconta", methods=["POST", "GET"])
def criar_conta():
    form_criarconta = CriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(email=form_criarconta.email.data, senha=senha, username=form_criarconta.username.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form = form_criarconta)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/perfil/<id_usuario>", methods=["POST", "GET"])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(int(id_usuario))
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = Path(Path(__file__).absolute().parent, app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data.desc()).all()
    return render_template("feed.html", fotos=fotos)