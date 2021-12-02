 import streamlit as st

 
 # Camisa Hombre
def camisas(datos_sexo, datos_talla):
    from PIL import Image
    if (datos_sexo == 'Masculino') & (datos_talla == 'Extra chica'):
        camisa_talla = Image.open('img/CAMISA_HOMBRE_base_xs.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Masculino') & (datos_talla == 'Chica'):
        camisa_talla = Image.open('img/CAMISA_HOMBRE_base_s.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Masculino') & (datos_talla == 'Mediana'):
        camisa_talla = Image.open('img/CAMISA_HOMBRE_base_m.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Masculino') & (datos_talla == 'Grande'):
        camisa_talla = Image.open('img/CAMISA_HOMBRE_base_g.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Masculino') & (datos_talla == 'Extra Grande'):
        camisa_talla = Image.open('img/CAMISA_HOMBRE_base_xl.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Masculino') & (datos_talla == '2X-L'):
        camisa_talla = Image.open('img/CAMISA_HOMBRE_base_2xl.png')
        st.image(camisa_talla, width=400)

            # Blusa Mujer
def blusas(datos_sexo, datos_talla):
    from PIL import Image
    if (datos_sexo == 'Femenino') & (datos_talla == 'Extra chica'):
        camisa_talla = Image.open('img/BLUSA_PARA_MUJER_base_xs.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Femenino') & (datos_talla == 'Chica'):
        camisa_talla = Image.open('img/BLUSA_PARA_MUJER_base_s.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Femenino') & (datos_talla == 'Mediana'):
        camisa_talla = Image.open('img/BLUSA_PARA_MUJER_base_m.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Femenino') & (datos_talla == 'Grande'):
        camisa_talla = Image.open('img/BLUSA_PARA_MUJER_base_g.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Femenino') & (datos_talla == 'Extra Grande'):
        camisa_talla = Image.open('img/BLUSA_PARA_MUJER_base_xl.png')
        st.image(camisa_talla, width=400)
    elif (datos_sexo == 'Femenino') & (datos_talla == '2X-L'):
        camisa_talla = Image.open('img/BLUSA_PARA_MUJER_base_2xl.png')
        st.image(camisa_talla, width=400)