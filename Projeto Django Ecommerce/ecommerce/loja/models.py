from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    nome =  models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=100, null=True, blank=True)
    id_sessao = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.email)


class Categoria(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.nome)

class Tipo(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.nome)


class Produto(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    tipo = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.nome} | Categoria: {self.categoria} | Tipo: {self.tipo} | Preço: {self.preco}"
    

    @property
    def qtd_vendida(self):
        itens = ItensPedido.objects.filter(pedido__finalizado=True, item_estoque__produto=self.id)
        qtd = sum([item.quantidade for item in itens])
        return qtd

class Cor(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    codigo = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self) -> str:
        return str(self.nome)

class ItemEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)
    cor = models.ForeignKey(Cor, null=True, blank=True, on_delete=models.SET_NULL)
    tamanho = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.produto.nome } | Cor: {self.cor} | Tamanho: {self.tamanho} | Quantidade: {self.quantidade}"

class Endereco(models.Model):
    rua = models.CharField(max_length=400, null=True, blank=True)
    numero = models.CharField(max_length=200, null=True, blank=True)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def get_campos(self):
        return [nome.name for nome in self._meta.fields]

    def __str__(self) -> str:
        return f'{self.cliente} | Rua: {self.rua}, {self.numero} |  Cep:{self.cep} | {self.cidade}-{self.estado}'

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    finalizado = models.BooleanField(default=False)
    codigo_transacao = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    data_finalizado = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'ID: {self.id} | {self.cliente} | Finalizado: {self.finalizado}'
    
    @property
    def quantidade_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido__id=self.id)
        total = sum([item.quantidade for item in itens_pedido])
        return total

    @property
    def valor_total(self):
        itens_pedido = ItensPedido.objects.filter(pedido__id=self.id)
        valor = sum([item.valor for item in itens_pedido])
        return valor
    
    @property
    def itens(self):
        itens_pedido = ItensPedido.objects.filter(pedido__id=self.id)
        return itens_pedido

class ItensPedido(models.Model):
    item_estoque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def valor(self):
        return self.quantidade * self.item_estoque.produto.preco

    def __str__(self) -> str:
        return f'ID Pedido: {self.pedido.id} | Produto: { self.item_estoque.produto.nome } | Cor {self.item_estoque.cor.nome} | Tamanho: {self.item_estoque.tamanho} | Quantidade: {self.quantidade}' 

class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino = models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.link_destino} | Ativo: {self.ativo}"
    
class Pagamento(models.Model):
    id_pagamento = models.CharField(max_length=400)
    pedido = models.ForeignKey(Pedido, blank = True, null=True, on_delete=models.SET_NULL)
    tipo_pagamento = models.CharField(max_length=400, blank=True, null=True)
    aprovado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.pedido.cliente} | Aprovado: {self.aprovado}'