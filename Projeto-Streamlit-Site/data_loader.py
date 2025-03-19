import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def carregar_base():
    df = pd.read_excel(Path(Path(__file__).absolute().parent,"Base.xlsx"))
    return df
