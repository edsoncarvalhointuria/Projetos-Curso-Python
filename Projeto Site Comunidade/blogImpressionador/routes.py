from blogImpressionador import app, database, bcrypt
from blogImpressionador.forms import FormCriarConta, FormFazerLogin, FormEditarPerfil, FormCriarPost
from blogImpressionador.models import Usuario, Post
from flask import render_template, flash, url_for, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from pathlib import Path
from PIL import Image
from datetime import datetime, timedelta



@app.route("/")
def homepage():
    posts = Post.query.order_by(Post.id.desc())
    return render_template("homepage.html", posts=posts, converter_data=converter_data)

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template("usuarios.html", lista_usuarios = lista_usuarios)

@app.route("/meus_posts")
@login_required
def meus_posts():
    return render_template("meus_posts.html", converter_data=converter_data)


@app.route("/login", methods=["POST", "GET"])
def login():
    form_login = FormFazerLogin()

    if form_login.validate_on_submit() and "botao_login" in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_acesso.data)
            flash("Login realizado com sucesso", category="alert-success")
            next_pg = request.args.get("next")
            if next_pg:
                return redirect(next_pg)
            else:
                return redirect(url_for('homepage'))
        else:
            flash("Falha no login. E-mail ou Senha incorretos", category="alert-danger")

    return render_template("login.html", form_login = form_login)

@app.route("/cadastrar", methods=["POST", "GET"])
def cadastra_se():
    form_cadastrase = FormCriarConta()
    if form_cadastrase.validate_on_submit() and "botao_cadastrar" in request.form:
        senha_bcrypt = bcrypt.generate_password_hash(form_cadastrase.senha.data).decode("utf-8")
        usuario = Usuario(username=form_cadastrase.username.data, email=form_cadastrase.email.data, senha=senha_bcrypt)
        database.session.add(usuario)
        database.session.commit()
        flash("Login realizado com sucesso", category="alert-success")
        login_user(usuario)
        return redirect(url_for('homepage'))
        
    return render_template("cadastrase.html", form_cadastrase=form_cadastrase)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout feito com sucesso", category="alert-success")
    return redirect(url_for("homepage"))


@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template("perfil.html", foto_perfil=foto_perfil)


@app.route("/post/criar", methods=["GET", "POST"])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(title = form.titulo.data, body=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash("Post realizado com sucesso", "alert-success")
        return redirect(url_for('homepage'))
    return render_template("criar_post.html", form=form)


def converter_data(data):
    fuso = timedelta(hours=datetime.now().astimezone().utcoffset().total_seconds()/3600)
    return data + fuso


@app.route("/post/<id_post>", methods=["GET", "POST"])
@login_required
def ver_post(id_post):
    form = FormCriarPost()
    post = Post.query.get(id_post)

    if request.method == "GET":
        form.titulo.data = post.title
        form.corpo.data = post.body
    elif form.validate_on_submit():
        post.title = form.titulo.data
        post.body = form.corpo.data
        flash("Post editado com sucesso", "alert-success")
        database.session.commit()
        return redirect(url_for('homepage'))
    return render_template("post.html", post=post, converter_data=converter_data, form=form)


@app.route("/post/<id_post>/excluir", methods=["GET", "POST"])
@login_required
def excluir_post(id_post):
    post = Post.query.get(id_post)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post excluido com sucesso", "alert-danger")
        return redirect(url_for('homepage'))
    else:
        abort(404)



def processar_imagem(foto):
    # Alterando o nome da imagem
    chave = secrets.token_hex(8)
    nome = Path(foto.filename)
    nome = nome.stem + chave + nome.suffix 

    # compactando a imagem
    tamanho = (400,400)
    imagem_reduzida = Image.open(foto).convert('RGB')
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(Path(app.root_path, 'static/fotos_perfil', nome))

    return nome


@app.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        if form.enviar_foto.data:
            imagem = processar_imagem(form.enviar_foto.data)
            current_user.foto_perfil = imagem

        cursos = [curso.label.text for curso in form if "curso" in curso.name and curso.data]
        if cursos:
            current_user.cursos = ";".join(cursos)
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        database.session.commit()
        flash("Perfil atualizado com sucesso", "alert-success")
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("editar_perfil.html", form=form)