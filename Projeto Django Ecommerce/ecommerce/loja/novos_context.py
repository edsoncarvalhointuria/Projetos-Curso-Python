from .models import Pedido, ItensPedido, Cliente, Categoria, Tipo


def carrinho(request):
    qtd_itens = 0
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        id_sessao = request.COOKIES.get('id_sessao')
        if id_sessao:
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return {'quantidade_itens':qtd_itens}
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    for item in itens_pedido:
        qtd_itens += item.quantidade
    return {'quantidade_itens':qtd_itens}

def lista_categorias(request):
    categorias_nav = Categoria.objects.all()
    tipos_nav = Tipo.objects.all()
    return {'categorias_nav': categorias_nav, 'tipos_nav': tipos_nav}

def faz_parte_equipe(request):
    equipe = False
    if request.user.is_authenticated and request.user.groups.filter(name='equipe').exists():
        equipe = True
    return {'faz_parte_equipe': equipe}
