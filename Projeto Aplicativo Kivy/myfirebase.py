import requests
from kivy.app import App
from api_key import API_KEY

class MyFireBase:

    def criar_conta(self, email, senha):
        link = f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}'
        info = {"email":email, "password":senha, "returnSecureToken":True}
        requisicao = requests.post(link, data=info)
        requisicao_dict = requisicao.json()

        if requisicao.ok:
            # requisicao_dict["idToken"] -> Autenticação (informação que limita a edição apenas para o usuário específico)
            # requisicao_dict["refreshToken"] -> TOKEN QUE MANTÉM O USUÁRIO LOGADO
            # requisicao_dict["localId"] -> ID DO USUARIO
            meu_app = App.get_running_app()
            id_token = requisicao_dict['idToken']
            meu_app.id_token = id_token
            meu_app.local_id = requisicao_dict['localId']
            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(requisicao_dict['refreshToken'])


            id_vendedor = requests.get(f'https://appvendas-ad187-default-rtdb.firebaseio.com/prox_id.json?auth={id_token}').json()

            link = f'https://appvendas-ad187-default-rtdb.firebaseio.com/{meu_app.local_id}.json?auth={id_token}'
            info_usuario = f'{{"avatar":"foto1.png", "equipe":"", "total_vendas":"0", "vendas":"", "id_vendedor":"{id_vendedor}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)
            
            prox_id_vendedor = int(id_vendedor) + 1
            info_id = f'{{"prox_id": "{prox_id_vendedor}"}}'
            requests.patch(f'https://appvendas-ad187-default-rtdb.firebaseio.com/.json?auth={id_token}', data=info_id)

            meu_app.atualizar_infos_usuario()
            meu_app.trocar_tela('homepage')

        else:
            erro = requisicao_dict['error']['message']
            meu_app = App.get_running_app()
            pg_login = meu_app.root.ids.get('loginpage')
            pg_login.ids.get('message_login').text = erro
            pg_login.ids.get('message_login').color = (1,0,0,1)
            



    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {"email": email, "password": senha, "returnSecureToken":True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        meu_app = App.get_running_app()

        if requisicao.ok:
            meu_app.id_token = requisicao_dic['idToken']
            meu_app.local_id = requisicao_dic['localId']
            with open('refreshtoken.txt', 'w') as arquivo:
                arquivo.write(requisicao_dic['refreshToken'])
            meu_app.atualizar_infos_usuario()
            meu_app.trocar_tela('homepage')
        else:
            
            login_page = meu_app.root.ids.get('loginpage')
            login_page.ids.get('message_login').text = requisicao_dic['error']['message']
            login_page.ids.get('message_login').color = (1,0,0,1)
    


    def validar_token(self, refresh_token):
        link = f'https://securetoken.googleapis.com/v1/token?key={self.API_KEY}'
        info = {'grant_type':'refresh_token', 'refresh_token':refresh_token}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if requisicao.ok:
            return requisicao_dic['id_token'], requisicao_dic['user_id']