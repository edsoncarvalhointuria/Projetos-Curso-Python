import streamlit as st
import pandas as pd


@st.cache_data
def carregar_base():
    df = pd.read_excel("Base.xlsx")
    return df
