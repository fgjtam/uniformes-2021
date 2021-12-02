import pandas as pd
import streamlit as st

@st.cache
def data():

    datos = pd.read_csv('./datasets/plantilla_fgj_2021-04-11_effm_v2.csv')
    datos['# EMP'].fillna(0, inplace=True)
    datos['# EMP'] = datos['# EMP'].astype(int)
    return datos