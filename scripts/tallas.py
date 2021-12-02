import pandas as pd
import streamlit as st
from datos import data


def dataframe_tallas(sexo, talla_nombre, talla_codigo, path_file):
    datos = data()                
    if (datos_sexo == sexo) & (datos_talla == talla_nombre):
        df_talla_camisas = pd.read_csv(path_file)
        df_talla_camisas[talla_codigo] = df_talla_camisas[talla_codigo].astype(str)
        df_talla_camisas.index = df_talla_camisas['Clave']
        df_camisas = st.table(df_talla_camisas[['Descripción',talla_codigo]])
        return df_camisas