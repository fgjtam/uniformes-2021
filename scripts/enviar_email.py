import smtplib
import time

def send_mail(email, folio, fecha, num_empleado, nombre, datos_municipio, datos_area, datos_talla):
    message = f"""From: Dirección General de Administración-FGJTAM <dga-fgjtam@outlook.com>
To: <{str(email)}>
MIME-Version: 1.0
Content-type: text/html;charset=utf-8
Subject: Confirmacion de registro No.{folio}

Se ha registrado su solicitud para la dotación de camisas institucionales.<br>
Fecha de solicitud: {str(fecha)}<br>
Folio: No.{folio}<br>
Número de empleado: {num_empleado}<br>
Nombre: {nombre}<br>
Municipio: {datos_municipio}<br>
Área: {datos_area}<br>
Talla: <b>{datos_talla}</b><br>

<h3>Fiscalía General de Justicia del Estado de Tamaulipas</h3>
<h4>Dirección General de Administración</h4>
""".encode('utf-8')
                        
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login('dga-fgjtam@outlook.com', '.F#adminTam.%#.')
    time.sleep(1)
    #print('Login success')
    server.sendmail('dga-fgjtam@outlook.com', email, message)
    #print('El email ha sido enviado.')
    server.quit()