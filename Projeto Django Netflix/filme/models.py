from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.

LISTA_CATEGORIAS = (
    ("ACAO", "Ação"),
    ("AVENTURA", "Aventura"),
    ("ROMANCE", "Romance"),
    ("OUTROS", "Outros")
)


class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_filme')
    descricao = models.TextField(max_length=1000)
    visualizacoes = models.IntegerField(default=0)
    data = models.DateTimeField(default= timezone.now)
    categoria = models.CharField(max_length=20, choices=LISTA_CATEGORIAS)
    filme = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo
    
    def name(self):
        return self.__class__.__name__
    

class Serie(Filme):
    filme = None

    

class Episodio(models.Model):
    serie = models.ForeignKey("Serie", on_delete=models.CASCADE, related_name="episodios")
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.titulo
    

class Usuario(AbstractUser):
    filmes_assistidos = models.ManyToManyField("Filme")

    

    
