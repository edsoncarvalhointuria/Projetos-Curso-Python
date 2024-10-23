import mercadopago
import os

public_key = os.getenv("MP_KEY")
token = os.getenv("MP_TOKEN")

def gerar_pagamento(itens, links):
    sdk = mercadopago.SDK(token)
    lista_itens = []
    for item in itens:
        quantidade = int(item.quantidade)
        valor = float(item.item_estoque.produto.preco)
        titulo = item.item_estoque.produto.nome
        lista_itens.append({'title': titulo,
         'quantity': quantidade,
         'unit_price': valor})


    preference_data = {
        "items": lista_itens,
        "back_urls": {
            "success": links,
            "failure": links,
            "pending": links
        }
    }

    preference_response = sdk.preference().create(preference_data)
    link = preference_response["response"]['init_point']
    id_pagamento = preference_response["response"]['id']
    return link, id_pagamento