from django.db.models import Min, Max
from .models import ItemEstoque
from django.core.mail import send_mail
import csv
from django.http import HttpResponse

def filtrar(produto, filtro):
    if filtro:
        if '-' in filtro:
            categoria, tipo = filtro.split('-')
            produto = produto.filter(categoria__slug=categoria, tipo__slug=tipo)
        else:
            produto = produto.filter(categoria__slug=filtro)
    return produto

def filtro_lateral(request, produtos):
    minimo, maximo = get_min_max(produtos)
    requisicoes = request.POST.dict()
    mn = requisicoes.get('preco_minimo')
    mx = requisicoes.get('preco_maximo')
    if mn == "":
        mn = minimo
    if mx == "" or float(mx) < minimo:
        mx= minimo
    produtos = produtos.filter(preco__gte=mn, preco__lte=mx)
    if "tamanho" in requisicoes:
        itens = ItemEstoque.objects.filter(produto__in = produtos, tamanho=requisicoes.get('tamanho'))
        itens = itens.values_list('produto', flat=True).distinct()
        produtos = produtos.filter(id__in=itens)
    if "tipo" in requisicoes:
        produtos = produtos.filter(tipo__slug=requisicoes.get('tipo'))
    if "categoria" in requisicoes:
        produtos = produtos.filter(categoria__slug=requisicoes.get('categoria'))
    return produtos

def get_min_max(produtos):
    minimo = 0
    maximo = 0
    if produtos:
        minimo = list(produtos.aggregate(Min('preco')).values())[0]
        minimo = round(minimo, 2)
        maximo = list(produtos.aggregate(Max('preco')).values())[0]
        maximo = round(maximo, 2)
    return minimo, maximo

def ordenar_produtos(produtos, ordem):
    if ordem == "menor-preco":
        produtos = produtos.order_by('preco')
    elif ordem == "maior-preco":
        produtos = produtos.order_by('-preco')
    elif ordem == "mais-vendidos":
        lista_prods = [(produto.qtd_vendida, produto) for produto in produtos]
        lista_prods = sorted(lista_prods, reverse=True, key=lambda item:item[0] )
        produtos = [produto[1] for produto in lista_prods]
    return produtos


def enviar_email(pedido):
    email = pedido.cliente.email
    subject = f"Pedido Aprovado: {pedido.codigo_transacao}"
    body = f'''Seu pedido foi aprovado.
ID Pedido:{pedido.id}
Valor Pedido: {pedido.valor_total}
'''
    de = 'edsoncarvalhointuria@gmail.com'
    send_mail(subject, body, de, [email])

def exportar(informacoes):
    resposta = HttpResponse(content_type='text/csv')
    resposta['Content-Disposition'] = f'attachment; filename={informacoes.model._meta}.csv'

    criador_csv = csv.writer(resposta, delimiter=';')

    colunas = informacoes.model._meta.fields
    colunas = [coluna.name for coluna in colunas]
    criador_csv.writerow(colunas)

    for item in informacoes.values_list():
        criador_csv.writerow(item)

    return resposta
