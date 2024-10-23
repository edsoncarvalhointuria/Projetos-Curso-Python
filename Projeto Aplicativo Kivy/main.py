from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
import certifi
from banner_vendas import BannerVendas
from banner_vendedor import BannerVendedor
import os
from myfirebase import MyFireBase
from functools import partial
from kivy.uix.popup import Popup
from datetime import datetime

# Criando variavel de ambiente para os links abrirem no celular (apenas links https)
os.environ["SSL_CERT_FILE"] = certifi.where()


GUI = Builder.load_file('main.kv')
class MainApp(App):

    def build(self):
        self.firebase = MyFireBase()
        self.select_cliente = None
        self.select_produto = None
        self.select_unidade = None
        return GUI
    
    def on_start(self):
        #Definindo Lista De Imagens
        alterar_foto_page = self.root.ids.get('alterarfotopage')
        lista_fotos = alterar_foto_page.ids.get('lista_alterar_imagens')
        for imagem in os.listdir('icones/fotos_perfil'):
            lista_fotos.add_widget(ImageButton(source=f'icones/fotos_perfil/{imagem}', on_release=partial(self.trocar_foto, imagem)))
        
        #Definindo Lista De Clientes
        adicionar_vendas_page = self.root.ids.get("adicionarvendaspage")
        lista_clientes = adicionar_vendas_page.ids.get("lista_clientes")
        for imagem in os.listdir('icones/fotos_clientes'):
            lista_clientes.add_widget(ImageButton(source=f"icones/fotos_clientes/{imagem}", on_release=partial(self.selecionar_texto, imagem, lista_clientes, "clientes")))
            lista_clientes.add_widget(LabelButton(text=imagem[:imagem.rindex('.')].capitalize(), on_release=partial(self.selecionar_texto, imagem, lista_clientes, "clientes")))
            
        #Definindo Lista De Produtos
        lista_produtos = adicionar_vendas_page.ids.get("lista_produtos")
        for imagem in os.listdir('icones/fotos_produtos'):
            lista_produtos.add_widget(ImageButton(source=f"icones/fotos_produtos/{imagem}", on_release=partial(self.selecionar_texto, imagem, lista_produtos, "produtos")))
            lista_produtos.add_widget(LabelButton(text=imagem[:imagem.rindex('.')].capitalize(), on_release=partial(self.selecionar_texto, imagem, lista_produtos, "produtos")))
            
        data = adicionar_vendas_page.ids.get('label_data')
        data.text = f"Data: {datetime.now().strftime('%d/%m/%Y')}"

        #Atualizando Infos Usuário
        try:
            with open('refreshtoken.txt', 'r') as arquivo:
                refresh_token = arquivo.read()
            id_token, local_id = self.firebase.validar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            self.atualizar_infos_usuario()
            self.trocar_tela('homepage')
        except AttributeError:
            pass
        except FileNotFoundError:
            pass

        return super().on_start()

    def atualizar_infos_usuario(self):
        requisicao = requests.get(f'https://appvendas-ad187-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}')
        requisicao = requisicao.json()

        homepage = self.root.ids.get('homepage')

        # PEGANDO VARIAVEIS DO USUARIO
        self.avatar = requisicao.get('avatar')
        self.total_vendas = requisicao.get('total_vendas')
        self.vendas = requisicao.get('vendas')
        self.id_vendedor = requisicao.get('id_vendedor')
        self.equipe = requisicao.get('equipe')

        self.definir_imagem(self.avatar)
        self.definir_total_vendas(homepage, self.total_vendas, self.vendas)
        self.definir_meu_id()
        self.definir_lista_equipe()


    def definir_imagem(self, avatar):
        
        imagem = self.root.ids.get('foto_perfil')
        imagem.source = f'icones/fotos_perfil/{avatar}'
    
    def label_total_vendas(self, page, valor_total):
        label_total_vendas = page.ids.get('label_total_vendas')
        label_total_vendas.text = f'[color=#000000]Total de Vendas:[/color] [b]R${float(valor_total):.2f}[/b]'

    def definir_total_vendas(self, page, valor_total_vendas, dic_vendas):
        # homepage = self.root.ids.get('homepage')
        self.label_total_vendas(page, valor_total_vendas)

        lista_vendas=  page.ids.get('lista_info_vendas')
        for key in dic_vendas:
            banner = BannerVendas(cliente = dic_vendas[key]['cliente'], data = dic_vendas[key]['data'], foto_cliente = dic_vendas[key]['foto_cliente'],
                            foto_produto = dic_vendas[key]['foto_produto'], preco = dic_vendas[key]['preco'], produto = dic_vendas[key]['produto'],
                            quantidade=dic_vendas[key]['quantidade'], unidade=dic_vendas[key]['unidade'])
            lista_vendas.add_widget(banner)

    def definir_meu_id(self):
        ajustes_page = self.root.ids.get('ajustespage')
        label_id_vendedor = ajustes_page.ids.get('id_vendedor')
        label_id_vendedor.text = f"Seu ID: {self.id_vendedor}"
    
    def definir_lista_equipe(self):
        ids_vendedores = self.equipe.split(',')
        listar_vendedores_page = self.root.ids.get('listarvendedorespage')
        lista_vendedores = listar_vendedores_page.ids.get('lista_vendedores')
        for id_vendedor in ids_vendedores:
            if id_vendedor != "":
                lista_vendedores.add_widget(BannerVendedor(id_vendedor = id_vendedor))
    
    def adicionar_vendedor(self, id_vendedor):
        requisicao = requests.get(f'https://appvendas-ad187-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"')
        requisicao_dic = requisicao.json()
        ac_vend_page = self.root.ids.get('acompanharvendedorpage')
        label_feedback = ac_vend_page.ids.get('feedback_search')

        listar_vendedores_page = self.root.ids.get('listarvendedorespage')
        lista_vendedores = listar_vendedores_page.ids.get('lista_vendedores')

        if not requisicao_dic:
            label_feedback.text = "Usuário não encontrado"
            label_feedback.color = (1,0,0,1)
            label_feedback.bold = True
        elif id_vendedor in self.equipe.split(','):
            label_feedback.text = "Usuário já faz parte da equipe"
            label_feedback.color = (1,0,0,1)
            label_feedback.bold = True
        else:
            self.equipe += f",{id_vendedor}"
            info = f'{{"equipe": "{self.equipe}"}}'
            requests.patch(f'https://appvendas-ad187-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}', data=info)
            label_feedback.text = "Usuário adicionado com sucesso"
            label_feedback.color = (0,1,0,1)
            label_feedback.bold = True

            lista_vendedores.add_widget(BannerVendedor(id_vendedor=id_vendedor))
    
    def trocar_tela(self, id_page, alterar_foto=False):
        if alterar_foto:
            self.definir_imagem(self.avatar)
        gerenciador_tela = self.root.ids['screen_manager']
        gerenciador_tela.current = id_page

    def trocar_foto(self, foto, *args):
        avatar = self.root.ids.get('foto_perfil')
        avatar.source = f"icones/fotos_perfil/{foto}"
        # teste = '{"avatar": "' + foto + '"}'
        image = f'{{"avatar":"{foto}"}}'
        requests.patch(f'https://appvendas-ad187-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}', data=image)
        self.avatar = foto
        self.trocar_tela('ajustespage')
    
    def selecionar_texto(self, imagem, item, tipo, *args):
        ad_vendas_page = self.root.ids.get("adicionarvendaspage")
        for widget in list(item.children):
            try:
                text = widget.text.lower() + '.png'
                if text == imagem or widget.text == imagem:
                    widget.color = (0,207/255,219/255,1)
                    widget.bold = True
                else:
                    widget.color = (1,1,1,1)
                    widget.bold = False

            except AttributeError:
                pass
        if tipo == "clientes":
            self.select_cliente = imagem
            ad_vendas_page.ids.get('label_selecionar_cliente').color = (1,1,1,1)
        elif tipo == "produtos":
            self.select_produto = imagem
            ad_vendas_page.ids.get('label_selecionar_produto').color = (1,1,1,1)
        elif tipo == "unidades":
            self.select_unidade = imagem


    def red_text(self, item):
        for label in list(item.children):
            label.color = (1,0,0,1)

    def adicionar_venda(self):
        texto_popup = ""
        ad_vend_page = self.root.ids.get("adicionarvendaspage")
        preco = ad_vend_page.ids.get("preco_total").text
        quantidade = ad_vend_page.ids.get("quantidade_total").text

        if not self.select_cliente:
            ad_vend_page.ids.get("label_selecionar_cliente").color = (1,0,0,1)
            texto_popup += "- Selecione um Cliente\n\n"
        if not self.select_produto:
            ad_vend_page.ids.get("label_selecionar_produto").color = (1,0,0,1)
            texto_popup += "- Selecione um Produto\n\n"
        if not self.select_unidade:
            self.red_text(ad_vend_page.ids.get("unidades"))
            texto_popup += "- Selecione a Unidade de Medida\n\n"
        if not preco:
            ad_vend_page.ids.get("label_preco_total").color = (1,0,0,1)
            texto_popup += "- Inclua o preço\n\n"
        else:
            ad_vend_page.ids.get("label_preco_total").color = (1,1,1,1)
        if not quantidade:
            ad_vend_page.ids.get("label_quantidade_total").color = (1,0,0,1)
            texto_popup += "- Inclua a quantidade\n\n"
        else:
            ad_vend_page.ids.get("label_quantidade_total").color = (1,1,1,1)
        

        if self.select_cliente and self.select_produto and self.select_unidade and preco and quantidade:
            info = f'{{"cliente":"{self.select_cliente.replace(".png", "").capitalize()}", "data":"{ad_vend_page.ids.get("label_data").text.replace("Data: ", "")}", "foto_cliente": "{self.select_cliente}", "foto_produto": "{self.select_produto}", "preco": "{preco}", "produto": "{self.select_produto.replace(".png", "").capitalize()}", "quantidade": "{quantidade}", "unidade": "{self.select_unidade}"}}'
            self.total_vendas = float(self.total_vendas)+float(preco)
            requests.post(f'https://appvendas-ad187-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}', data=info)
            info = f'{{"total_vendas":"{self.total_vendas}"}}'
            requests.patch(f'https://appvendas-ad187-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}', data=info)

            homepage = self.root.ids.get('homepage')
            lista_vendas=  homepage.ids.get('lista_info_vendas')
            banner = BannerVendas(cliente = self.select_cliente.replace(".png", "").capitalize(), data = ad_vend_page.ids.get("label_data").text.replace("Data: ", ""), foto_cliente = self.select_cliente,
                            foto_produto = self.select_produto, preco = preco, produto = self.select_produto.replace(".png", "").capitalize(),
                            quantidade=quantidade, unidade=self.select_unidade)
            lista_vendas.add_widget(banner)
            self.label_total_vendas(homepage, self.total_vendas)
            self.trocar_tela('homepage')
        else:
            popup = Popup(title='Dados Incompletos', content=Label(text=texto_popup), size_hint=(None, None), size=(300, 350))
            popup.open()
    
    def ver_todas_vendas(self):
        todas_vendas_page = self.root.ids.get('vertodasvendaspage')
        requisicao = requests.get('https://appvendas-ad187-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_dic = requisicao.json()
        total_vendas = 0

        todas_vendas_page.ids.get("lista_info_vendas").clear_widgets()
    
        for key in requisicao_dic:
            usuario = requisicao_dic[key]
            if key != "prox_id":
                total_vendas += float(usuario.get("total_vendas"))
                self.definir_total_vendas(todas_vendas_page, total_vendas, usuario.get('vendas'))
        self.definir_imagem('logo1.png')
        self.trocar_tela('vertodasvendaspage')

    def ver_outro_vendedor(self, vendedor_dic, *args):
        outro_vendedor_page = self.root.ids.get('veroutrovendedorpage')
        outro_vendedor_page.ids.get('lista_info_vendas').clear_widgets()
        self.definir_total_vendas(outro_vendedor_page, vendedor_dic.get('total_vendas'), vendedor_dic.get('vendas'))
        self.definir_imagem(vendedor_dic.get('avatar'))
        self.trocar_tela('veroutrovendedorpage')
      




MainApp().run()