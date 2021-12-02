import streamlit as st
import pandas as pd
from datetime import date
import sqlite3
from sqlite3.dbapi2 import IntegrityError, OperationalError
from PIL import Image
import smtplib
import time
import scripts.datos
import scripts.enviar_email
#import pyautogui

fecha = date.today()

# Conexión db
con = sqlite3.connect('db/fgj_uniformes.db')
cur = con.cursor()

# Configuración de página
st.set_page_config(page_title='Fiscalía General de Justicia del Estado de Tamaulipas', page_icon='⚖️')
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Datos caché
datos = scripts.datos.data()
policias = datos[ 
    (datos['PUESTO']=='AGENTE POLICIA INVESTIGADOR') | 
    (datos['PUESTO']=='AGENTE SUBOFICIAL "B"') | 
    (datos['PUESTO']=='COMISARIO GENERAL DE INVESTIGACION') | 
    (datos['PUESTO']=='A.P.M. / ESCOLTA') | 
    (datos['PUESTO']=='INSPECTOR GENERAL') | 
    (datos['PUESTO']=='AGENTE POLICIA MINISTERIAL') | 
    (datos['PUESTO']=='COMANDANTE') | 
    (datos['PUESTO']=='JEFE DE GRUPO') | 
    (datos['PUESTO']=='COMISARIO') ]

policias = policias[ (policias['ESTATUS']=='ACTIVO') ]
policias_num_empleado = policias['# EMP'].astype(int)
registrados = pd.read_sql('select * from uniformes;', con)
empleados_registrados = registrados['num_empleado'].astype(int)

# Logo
logo = Image.open('img/logo_ch.png')
st.image(logo, width=200)
#st.markdown('___')

# Columnas
col1, col2 = st.columns(2)

with col1:
    form1 = st.form(key='formulario1')
    num_empleado = form1.text_input('Ingrese su número de empleado: ')
    boton_num_empleado = form1.form_submit_button('Buscar')

try:
    if (boton_num_empleado) and (int(num_empleado) not in list(datos['# EMP'])):
        st.error('Favor de comunicarse a la Dirección de Recursos Humanos, para verificar su número de empleado')
    elif boton_num_empleado and int(num_empleado) in list(empleados_registrados):
        st.info('Le informamos que ya se encuentra una solicitud registrada a su nombre.')
    elif boton_num_empleado and (int(num_empleado) in list(policias_num_empleado)):
        policias_puesto = policias[ policias['# EMP']==int(num_empleado) ]
        policias_puesto = policias_puesto.iloc[0,7]
        st.info(f'Su puesto es {policias_puesto}. En este ejercicio solo se proporcionarán uniformes al personal administrativo, posteriormente se realizará un ejercicio para el personal policial.')
    elif num_empleado:
        datos = scripts.datos.data()
        datos_empleado = datos[ datos['# EMP']==int(num_empleado) ]                      
        st.markdown('**Nombre: **')
        nombre = st.write(datos_empleado.iloc[0,15])
        nombre = datos_empleado.iloc[0,15]
        st.markdown('**Puesto: **')
        puesto = st.write(datos_empleado.iloc[0,7])
        puesto = datos_empleado.iloc[0,7]
        st.markdown('**Sexo**:')
        datos_sexo = st.radio('Seleccionar: ',['Masculino', 'Femenino'])
        
        with st.container():
    
            col1_container_1, col2_container_2 = st.columns(2)
    
            with col1_container_1:
                st.markdown('**Celular:**')
                celular = st.text_input('Ingrese su número de Celular:', help='Ingrese los 10 dígitos de su número de celular, sin guiones ni espacios', max_chars=10)
                #celular = st.number_input('Ingresa tu número de Celular:', help='Ingrese los 10 dígitos de su número de celular, sin guiones ni espacios', step=None, value=0)
                if not celular:
                    st.error('Este campo es obligatorio.')
                
            with col2_container_2:
                st.markdown('**Correo electrónico:**')
                email = st.text_input('Ingrese su correo:', help='Es necesario para que se envien los datos de registro. Puede ingresar el correo Institucional o Personal')
                email = str(email)
                if not email:
                    st.error('Este campo es obligatorio.')
        st.markdown('**Municipio**:')
        datos_municipio = st.selectbox('Seleccionar Municipio:', datos['MUNICIPIO'].unique())
        lista_areas_por_direccion = list(datos['DIRECCION'].unique())
        lista_areas_por_direccion.sort()
        st.markdown('**Dirección**:')
        datos_area = st.selectbox('Seleccionar Dirección:', lista_areas_por_direccion)
    
        with st.container():
    
            col1_container, col2_container = st.columns(2)
    
            with col1_container:
                st.write('')
                st.write('')
                st.write('')
                
                st.markdown('**Talla de Camisas o Blusas**:')
                #datos_talla = st.select_slider('Seleccione su talla: ', options=['Extra chica', 'Chica', 'Mediana', 'Grande', 'Extra Grande', '2X-G'])
                datos_talla = st.radio('Seleccione su talla: ', options=['Extra chica', 'Chica', 'Mediana', 'Grande', 'Extra Grande', '2X-G'])
                def dataframe_tallas(sexo, talla_nombre, talla_codigo, path_file):
                
                    if (datos_sexo == sexo) & (datos_talla == talla_nombre):
                        df_talla_camisas = pd.read_csv(path_file)
                        df_talla_camisas[talla_codigo] = df_talla_camisas[talla_codigo].astype(str)
                        df_talla_camisas.index = df_talla_camisas['Clave']
                        df_camisas = st.table(df_talla_camisas[['Descripción',talla_codigo]])
                        return df_camisas

                # Camisas de Hombre Data Frame
                dataframe_tallas('Masculino', 'Extra chica', 'XS', 'datasets/talla_camisas.csv')
                dataframe_tallas('Masculino', 'Chica', 'S', 'datasets/talla_camisas.csv')
                dataframe_tallas('Masculino', 'Mediana', 'M', 'datasets/talla_camisas.csv')
                dataframe_tallas('Masculino', 'Grande', 'G', 'datasets/talla_camisas.csv')
                dataframe_tallas('Masculino', 'Extra Grande', 'XG', 'datasets/talla_camisas.csv')
                dataframe_tallas('Masculino', '2X-G', '2XG', 'datasets/talla_camisas.csv')
    
                # Blusas de Mujer Data Frame
                dataframe_tallas('Femenino', 'Extra chica', 'XS', 'datasets/talla_blusas.csv')
                dataframe_tallas('Femenino', 'Chica', 'S', 'datasets/talla_blusas.csv')
                dataframe_tallas('Femenino', 'Mediana', 'M', 'datasets/talla_blusas.csv')
                dataframe_tallas('Femenino', 'Grande', 'G', 'datasets/talla_blusas.csv')
                dataframe_tallas('Femenino', 'Extra Grande', 'XG', 'datasets/talla_blusas.csv')
                dataframe_tallas('Femenino', '2X-G', '2XG', 'datasets/talla_blusas.csv')
             
            with col2_container:

                def imagenes_tallas(sexo, talla_nombre, path_file):
                
                    if (datos_sexo == sexo) & (datos_talla == talla_nombre):
                        camisa_talla = Image.open(path_file)
                        return st.image(camisa_talla, width=400)

                # Camisas Hombre (img)
                imagenes_tallas('Masculino', 'Extra chica', 'img/CAMISA_HOMBRE_base_xs.png')
                imagenes_tallas('Masculino', 'Chica', 'img/CAMISA_HOMBRE_base_s.png')
                imagenes_tallas('Masculino', 'Mediana', 'img/CAMISA_HOMBRE_base_m.png')
                imagenes_tallas('Masculino', 'Grande', 'img/CAMISA_HOMBRE_base_g.png')
                imagenes_tallas('Masculino', 'Extra Grande', 'img/CAMISA_HOMBRE_base_xl.png')
                imagenes_tallas('Masculino', '2X-G', 'img/CAMISA_HOMBRE_base_2xl.png')
    
                # Blusas Mujer (img)
                imagenes_tallas('Femenino', 'Extra chica', 'img/BLUSA_PARA_MUJER_base_xs.png')
                imagenes_tallas('Femenino', 'Chica', 'img/BLUSA_PARA_MUJER_base_s.png')
                imagenes_tallas('Femenino', 'Mediana', 'img/BLUSA_PARA_MUJER_base_m.png')
                imagenes_tallas('Femenino', 'Grande', 'img/BLUSA_PARA_MUJER_base_g.png')
                imagenes_tallas('Femenino', 'Extra Grande', 'img/BLUSA_PARA_MUJER_base_xl.png')
                imagenes_tallas('Femenino', '2X-G', 'img/BLUSA_PARA_MUJER_base_2xl.png')
                                
            col2_container.markdown(f'Confirmo que mi selección de blusa o camisa es talla: **{datos_talla}**')
            confirmacion = col2_container.checkbox('Confirmar', help='No habrá cambios de tallas al momento de la entrega. Se recomienda cehcar sus medidas según la guía de tallas de este formulario.')
            
            if not confirmacion:
                col2_container.warning('Favor de confirmar la talla de su camisa.')
            elif confirmacion and (not email) or (not celular):
                col2_container.error('Favor de ingresar todos los campos requeridos (celular y/o email).')
            elif confirmacion:
                boton_enviar_solicitud = col2_container.button('Enviar', key='boton_enviar', help='Una vez enviado no habrá cambios ni modificaciones' )
    
                if boton_enviar_solicitud:
                    try:
                        cur.execute("insert into uniformes (fecha, num_empleado, nombre, email, celular, puesto, sexo, municipio, area_direccion, talla, confirmacion) values (?,?,?,?,?,?,?,?,?,?,?)", (fecha,num_empleado,nombre,email,celular,puesto,datos_sexo,datos_municipio,datos_area,datos_talla,confirmacion,))
                        con.commit()
                        folio_db = cur.execute('select id from uniformes where num_empleado=?',(num_empleado,))
                        con.commit()

                        for folio in folio_db:
                            folio = str(folio[0])                                                
                        st.success(f'¡Gracias! Tu solicitud ha sido registrada con el Folio No. {folio}...')
    
                        # Confirmación vía email
                        scripts.enviar_email.send_mail(email, folio, fecha, num_empleado, nombre, datos_municipio, datos_area, datos_talla)
                        con.close()    
    
                        st.success(f'La confirmación de registro se ha enviado a su email...')
                        st.success('Favor de actualizar la página para añadir un nuevo registro')
                        #pyautogui.hotkey("ctrl","F5")
    
                    except IntegrityError:
                        st.info('Ya existe un registro para este número de usuario')
                    except OperationalError:
                        st.error('Registro existente, favor de actualizar la página web.')
                    except UnicodeEncodeError:
                        st.error('Verifica tu email')
                    except smtplib.SMTPAuthenticationError:
                        st.error('El servidor de correo no se encuentra disponible, pero su solicitud ya ha sido registrada')

except ValueError:
    st.error('Favor de ingresar solo números')