import pandas as pd
import streamlit as st
import joblib
# streamlit run deploy-teste.py

x_values = {"host_listings_count":0, "latitude":0, "longitude":0, "accommodates":0, "bathrooms":0, "bedrooms":0, "beds":0, "amenities":0, 
             "extra_people":0, "minimum_nights":0, "mes":0, "ano":0}

x_tf = {"host_is_superhost":0, "instant_bookable":0}

x_list = {"cancellation_policy": ["flexible", "moderate", "strict", "strict_14_with_grace_period"],
           "room_type":["Entire home/apt", "Hotel room", "Private room", "Shared room"],
           "property_type": ["Apartment", "Bed and breakfast", "Condominium", "Guest suite", "Guesthouse", "Hostel", "House", "Loft", "Other", "Serviced apartment"]}

dicionario = {f"{item}_{item_lista}":0 for item in x_list for item_lista in x_list[item]}


for item in x_values:
    if item == "latitude" or item == "longitude":
        valor = st.number_input(f"{item}", step=0.00001, value=0.0, format="%.5f")
    elif item == "extra_people":
        valor = st.number_input(f"{item}", step=0.1, value=0.0)
    else:
        valor = st.number_input(f"{item}", step=1, value=0)
    x_values[item] = valor

for item in x_tf:
    valor = st.selectbox(f"{item}", ("SIM", "NÃO"))
    if valor == "SIM":
        x_tf[item] = 1
    else:
        x_tf[item] = 0

for item in x_list:
    valor = st.selectbox(f"{item}", x_list[item])
    dicionario[f"{item}_{valor}"] = 1

botao = st.button("Calcular Valor Imovel")

if botao:
    dicionario.update(x_tf)
    dicionario.update(x_values)
    colunas = ['host_is_superhost', 'host_listings_count', 'latitude', 'longitude',
        'accommodates', 'bathrooms', 'bedrooms', 'beds', 'amenities',
        'extra_people', 'minimum_nights', 'instant_bookable', 'mes', 'ano',
        'cancellation_policy_flexible', 'cancellation_policy_moderate',
        'cancellation_policy_strict',
        'cancellation_policy_strict_14_with_grace_period',
        'room_type_Entire home/apt', 'room_type_Hotel room',
        'room_type_Private room', 'room_type_Shared room',
        'property_type_Apartment', 'property_type_Bed and breakfast',
        'property_type_Condominium', 'property_type_Guest suite',
        'property_type_Guesthouse', 'property_type_Hostel',
        'property_type_House', 'property_type_Loft', 'property_type_Other',
        'property_type_Serviced apartment']
    df = pd.DataFrame(dicionario, index=[0])
    df = df[colunas]
    modelo = joblib.load("modelo.joblib")
    preco = modelo.predict(df)
    st.write(preco[0])