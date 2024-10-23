from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle


class BannerVendas(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.cols=3
        self.rows=1
        self.padding = (0,10,0,0)
        cliente = kwargs['cliente']
        data = kwargs['data']
        foto_cliente= kwargs['foto_cliente']
        foto_produto = kwargs['foto_produto']
        preco = float(kwargs['preco'])
        produto = kwargs['produto']
        quantidade = kwargs['quantidade']
        unidade = kwargs['unidade']


        with self.canvas:
            Color(rgb = (0,0,0,1))
            self.rec = Rectangle(size = self.size, pos = self.pos)
        self.bind(pos = self.atualizar_canvas, size=self.atualizar_canvas)

        esquerda = GridLayout(rows=2)
        imagem_cliente = Image(source =f'icones/fotos_clientes/{foto_cliente}')
        label_cliente = Label(text=cliente)
        esquerda.add_widget(imagem_cliente)
        esquerda.add_widget(label_cliente)
        self.add_widget(esquerda)

        centro = GridLayout(rows=2)
        imagem_produto = Image(source=f'icones/fotos_produtos/{foto_produto}')
        label_produto = Label(text=produto)
        centro.add_widget(imagem_produto)
        centro.add_widget(label_produto)
        self.add_widget(centro)


        direita = GridLayout(rows=3, padding=(0,0,50,10))
        label_info_produto = Label(text=f'Data: {data}')
        direita.add_widget(label_info_produto)
        label_info_produto = Label(text=f'Preço: R${preco:.2f}')
        direita.add_widget(label_info_produto)
        label_info_produto = Label(text=f'{quantidade} {unidade}')
        direita.add_widget(label_info_produto)
        self.add_widget(direita)

    def atualizar_canvas(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size