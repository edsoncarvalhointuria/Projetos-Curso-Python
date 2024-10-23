from botoes import *
import requests
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from functools import partial
from kivy.graphics import Color, Rectangle
from kivy.app import App


class BannerVendedor(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()
        id_vendedor = kwargs['id_vendedor']

        with self.canvas:
            Color(rgb=(0,0,0,1))
            self.rec = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.atualizar_canvas, size=self.atualizar_canvas)

        layout = GridLayout(rows=1, padding=(9,9,9,9), size_hint = (0.8, 1), pos_hint={"right":0.9, "top": 1})

        requisicao = requests.get(f'https://appvendas-ad187-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"')
        requisicao_dic = requisicao.json()
        vendedor = list(requisicao_dic.values())[0]
        avatar = vendedor['avatar']
        total_vendas = vendedor['total_vendas']
        meu_app = App.get_running_app()

        imagem = ImageButton(source=f'icones/fotos_perfil/{avatar}', on_release=partial(meu_app.ver_outro_vendedor, vendedor))
        layout.add_widget(imagem)

        labels = GridLayout(rows=2, spacing=(-30,-30))
        label = LabelButton(text=f"ID Vendedor: {id_vendedor}", on_release=partial(meu_app.ver_outro_vendedor, vendedor))
        labels.add_widget(label)
        label = LabelButton(text=f"Total de Vendas: R${total_vendas}", on_release=partial(meu_app.ver_outro_vendedor, vendedor))
        labels.add_widget(label)
        layout.add_widget(labels)
        self.add_widget(layout)

    def atualizar_canvas(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size
        