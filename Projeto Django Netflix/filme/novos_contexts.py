from .models import Filme
from random import randint

def filmes_em_alta(request):
    em_alta = Filme.objects.all().order_by("-visualizacoes")[:8]
    return {"filmes_em_alta":em_alta}


def filmes_recentes(request):
    recentes = Filme.objects.all().order_by("-data")[:8]
    return {"filmes_recentes":recentes}

def filme_em_destaque(request):
    filme = Filme.objects.all()
    if filme:
        filme = Filme.objects.get(id=randint(1, len(filme)))
    else:
        filme = None
    return {"filme_destaque":filme}

def categoria(request):
    filmes = Filme.objects.all()
    categorias = set(sorted(filme.get_categoria_display() for filme in filmes))
    return {"categorias":categorias}