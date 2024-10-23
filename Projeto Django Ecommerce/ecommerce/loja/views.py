from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import *
import uuid
from .utils import *
from datetime import datetime
from .api_mp import gerar_pagamento


NOME_ID_SESSAO = 'id_sessao'

# Create your views here.
def homepage(request):
    banners = Banner.objects.filter(ativo=True)
    context={"banners":banners}
    return render(request, 'homepage.html',context)

def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True)
    produtos = filtrar(produtos, filtro)
    if request.method == "POST":
        produtos = filtro_lateral(request, produtos)

    minimo, maximo = get_min_max(produtos)
    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    tamanhos = itens.values_list('tamanho', flat=True).distinct()
    categorias = produtos.values_list('categoria', flat=True).distinct()
    categorias = Categoria.objects.filter(id__in=categorias)
    tipos = produtos.values_list('tipo', flat=True).distinct()
    tipos = Tipo.objects.filter(id__in=tipos)
    ordem = request.GET.get('order', 'menor-preco')
    produtos = ordenar_produtos(produtos, ordem)
    context = {"produtos":produtos, "minimo":str(minimo), "maximo":str(maximo), "tamanhos": tamanhos, 
               'categorias':categorias, 'tipos':tipos}
    return render(request, 'loja.html', context)

def ver_produto(request, pk_produto, pk_cor=None):
    cor_selecionada = None
    tamanhos = None
    produto = Produto.objects.get(id=pk_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)
    cores = {item.cor for item in itens_estoque}
    produtos_semelhantes = Produto.objects.filter(categoria = produto.categoria).exclude(id=produto.id)[:4]

    if pk_cor:
        itens_estoque = itens_estoque.filter(cor__id=pk_cor)
        cor_selecionada = Cor.objects.get(id=pk_cor)
        tamanhos = {item.tamanho for item in itens_estoque}

    context = {'produto':produto, "itens_estoque":itens_estoque, "cores":cores, "cor_selecionada":cor_selecionada,
                "tamanhos":tamanhos, 'produtos_semelhantes':produtos_semelhantes}
    return render(request, 'ver_produto.html', context)

def adicionar_carrinho(request, pk_produto):
    if request.method == "POST" and pk_produto:
        requisicoes = request.POST.dict()
        tamanho = requisicoes.get('tamanho')
        cor = requisicoes.get('cor')
        if not tamanho:
            return redirect('ver_produto', pk_produto)
        resposta = redirect('carrinho')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            id_sessao = request.COOKIES.get(NOME_ID_SESSAO)
            if not id_sessao:
                id_sessao = uuid.uuid4()
                resposta.set_cookie(key=NOME_ID_SESSAO, value=id_sessao, max_age=60*60*24*7)
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)

        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque= ItemEstoque.objects.get(cor__id=cor, tamanho=tamanho, produto_id=pk_produto)
        item_pedido, criado = ItensPedido.objects.get_or_create(pedido=pedido, item_estoque=item_estoque)
        item_pedido.quantidade += 1
        item_pedido.save()

        return resposta
    else:
        return redirect('loja')
    
def remover_carrinho(request, pk_produto):
    if request.method == "POST" and pk_produto:
        requisicoes = request.POST.dict()
        cor = requisicoes.get('cor')
        tamanho = requisicoes.get('tamanho')
        if not tamanho or not cor:
            return redirect('carrinho')
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            id_sessao = request.COOKIES.get(NOME_ID_SESSAO)
            if id_sessao:
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(cor__id=cor, tamanho=tamanho, produto__id=pk_produto)
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade -= 1
        item_pedido.save()
        if item_pedido.quantidade < 1:
            item_pedido.delete()
        return redirect('carrinho')


def carrinho(request): 
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        id_sessao = request.COOKIES.get(NOME_ID_SESSAO)
        if id_sessao:
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return render(request, 'carrinho.html', context={'cliente_existe':False})
    pedido, criado = Pedido.objects.get_or_create(cliente = cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido).select_related('item_estoque__produto', 'item_estoque__cor')
    context = {'pedido':pedido, 'itens_pedido':itens_pedido, 'cliente_existe':True}
    return render(request, 'carrinho.html', context)

def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        id_sessao = request.COOKIES.get(NOME_ID_SESSAO)
        if id_sessao:
            cliente = Cliente.objects.get(id_sessao=id_sessao)
        else:
            return redirect('loja')
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {"pedido":pedido, "enderecos":enderecos, "cliente":cliente}
    return render(request, 'checkout.html', context)

def finalizar_pedido(request, id_pedido):
    erro = None
    if request.method == "POST":
        pedido = Pedido.objects.filter(id=id_pedido, finalizado=False)
        if pedido:
            pedido = pedido.first()
            requisicoes = request.POST.dict()
            endereco = requisicoes.get('endereco')

            if not endereco:
                erro = 'endereco'
            else:
                pedido.endereco = Endereco.objects.get(id=endereco)

            if float(pedido.valor_total) != float(requisicoes.get('valor').replace('.', '').replace(',', '.')):
                erro = 'valores'
            elif not request.user.is_authenticated:
                try:
                    email = requisicoes.get('email')
                    validate_email(email)
                    clientes = Cliente.objects.filter(email = email)
                    if clientes:
                        pedido.cliente = clientes.first()
                    else:
                        pedido.cliente.email = email
                        pedido.cliente.save()
                except ValidationError:
                    erro = "email"
            
            pedido.codigo_transacao = f'{pedido.id}-{datetime.now().timestamp()}'
            pedido.save()
            if erro:
                enderecos = Endereco.objects.filter(cliente = pedido.cliente)
                context = {'erro': erro, 'pedido':pedido, 'enderecos':enderecos, 'cliente':pedido.cliente}
                return render(request, 'checkout.html', context)
            else:
                itens_pedido = ItensPedido.objects.filter(pedido=pedido)
                links = request.build_absolute_uri(reverse('finalizar_pagamento'))
                link, id_pagamento = gerar_pagamento(itens_pedido, links)
                pagamento = Pagamento.objects.create(id_pagamento = id_pagamento, pedido = pedido)
                pagamento.save()
                return redirect(link)
        else:
            return redirect('carrinho')
    else:
        return redirect('checkout')

def finalizar_pagamento(request):
    requisicoes = request.GET.dict()
    id_pagamento = requisicoes.get('preference_id')
    status = requisicoes.get('status')
    if id_pagamento and status=="approved":
        pagamento = Pagamento.objects.get(id_pagamento = id_pagamento)
        pagamento.aprovado = True
        pagamento.tipo_pagamento = requisicoes.get('payment_type')
        pagamento.save()
        pedido = pagamento.pedido
        pedido.finalizado = True
        pedido.data_finalizado = datetime.now()
        pedido.save()
        enviar_email(pedido)

        if request.user.is_authenticated:
            return redirect('meus_pedidos')
        else:
            return redirect('pedido_aprovado', pedido.id)
    else:
        return redirect('carrinho')
    
def pedido_aprovado(request, id_pedido):
    pedido = Pedido.objects.get(id=id_pedido)
    context = {"pedido" : pedido, "itens_pedido":ItensPedido.objects.filter(pedido=pedido)}
    return render(request, 'pedido_aprovado.html', context)

def adicionar_endereco(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            cliente = request.user.cliente
            print("entrei aqui")
        else:
            id_sessao = request.COOKIES.get(NOME_ID_SESSAO)
            if id_sessao:
                cliente = Cliente.objects.get(id_sessao=id_sessao)
            else:
                redirect('loja')
        requisicoes = request.POST.dict()
        rua = requisicoes.get('rua')
        numero = requisicoes.get('numero')
        cep = requisicoes.get('cep')
        cidade = requisicoes.get('cidade')
        estado = requisicoes.get('estado')
        if rua and numero and cep and cidade and estado:
            endereco = Endereco.objects.create(cliente=cliente, rua=rua, numero=numero, cep=cep, cidade=cidade, estado=estado, complemento=requisicoes.get('complemento'))
            return redirect('checkout')
        else:
            return render(request, 'adicionar_endereco.html')
    else:
        return render(request, 'adicionar_endereco.html')


def fazer_login(request):
    erro = False
    if request.user.is_authenticated:
        return redirect('loja')
    elif request.method == "POST":
        requisicoes = request.POST.dict()
        if 'email' in requisicoes and 'senha' in requisicoes:
            username = requisicoes.get('email')
            password = requisicoes.get('senha')
            usuario = authenticate(request, username=username, password=password)
            if usuario:
                login(request, usuario)
                return redirect('loja')
            else:
                erro = True
        else:
            erro = True
    return render(request, 'usuario/fazer_login.html', context={'erro':erro})

def criar_conta(request):
    erro = None
    if request.user.is_authenticated:
        return redirect('loja')
    elif request.method == "POST":
        requisicoes = request.POST.dict()
        if "email" in requisicoes and "senha" in requisicoes and "confirmacao_senha" in requisicoes:
            email = requisicoes.get('email')
            senha = requisicoes.get('senha')
            conf_senha = requisicoes.get('confirmacao_senha')
            try:
                validate_email(email)
                if senha == conf_senha:
                    usuario, criado = User.objects.get_or_create(username=email, email=email)
                    if not criado:
                        erro = "email_cadastrado"
                    else:
                        usuario.set_password(senha)
                        usuario.save()
                        login(request, usuario)

                        id_sessao = request.COOKIES.get(NOME_ID_SESSAO)
                        if id_sessao:
                            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
                        else:
                            cliente, criado = Cliente.objects.get_or_create(email=email)
                        
                        cliente.email = email
                        cliente.usuario = usuario
                        cliente.save()
                        return redirect('loja')
                else:
                    erro = "Senhas Diferentes"

            except ValidationError:
                erro = "E-mail Invalido"
        else:
            erro = "Preenchimento Invalido"

    context = {"erro":erro}
    return render(request, 'usuario/criar_conta.html', context)

@login_required
def minha_conta(request):
    erro_senha = None
    erro_dados = None
    mensagem_senha = None
    mensagem_dados = None
    if request.method == "POST":
        requisicoes = request.POST.dict()
        if 'senha_atual' in requisicoes:
            senha_atual = requisicoes.get('senha_atual')
            nova_senha = requisicoes.get('nova_senha')
            conf_senha = requisicoes.get('nova_senha_confirmacao')
            if nova_senha == conf_senha:
                usuario = authenticate(request, username=request.user.username, password=senha_atual)
                if usuario:
                    usuario.set_password(nova_senha)
                    usuario.save()
                    login(request, usuario)
                    mensagem_senha = "Senha Alterada Com Sucesso"
                else:
                    erro_senha = 'Senha Atual Incorreta'
            else:
                erro_senha = "Senhas Diferentes"
        elif 'email' in requisicoes:
            nome = requisicoes.get('nome')
            email = requisicoes.get('email')
            telefone = requisicoes.get('telefone')
            if email != request.user.email:
                usuario = User.objects.filter(email=email)
                if usuario:
                    erro_dados = "E-mail Já Cadastrados"

            if not erro_dados:
                try:
                    validate_email(email)
                    cliente = request.user.cliente
                    usuario = request.user

                    cliente.telefone = telefone
                    cliente.nome = nome
                    cliente.email = email
                    usuario.username = email
                    usuario.email = email

                    cliente.save()
                    usuario.save()
                    mensagem_dados = "Dados Alterados"

                except ValidationError:
                    erro_dados = "E-mail Invalido"
            
    context = {'erro_dados':erro_dados, 'erro_senha':erro_senha, 'mensagem_senha':mensagem_senha, 'mensagem_dados':mensagem_dados}
    return render(request, 'usuario/minha_conta.html', context)

@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user.cliente, finalizado=True).order_by('-data_finalizado')

    context = {'pedidos':pedidos}
    return render(request, 'usuario/meus_pedidos.html', context)

@login_required
def fazer_logout(request):
    logout(request)
    return redirect('fazer_login')

@login_required
def gerenciar_loja(request):
    if request.user.groups.filter(name='equipe').exists():
        pedidos = Pedido.objects.filter(finalizado=True)
        faturamento = sum(pedido.valor_total for pedido in pedidos)
        produtos = sum(pedido.quantidade_total for pedido in pedidos)
        context = {"pedidos":len(pedidos), "produtos":produtos, "faturamento":faturamento}
        return render(request, 'interno/gerenciar_loja.html', context)
    else:
        return redirect('loja')
    
@login_required
def exportar_relatorio(request, solicitacao):
    if request.user.groups.filter(name='equipe').exists():
        if solicitacao == 'pedidos':
            informacoes = Pedido.objects.filter(finalizado=True)
        elif solicitacao == 'clientes':
            informacoes = Cliente.objects.all()
        elif solicitacao == 'enderecos':
            informacoes = Endereco.objects.all()
    
        return exportar(informacoes)
    else:
        return redirect('loja')
 
