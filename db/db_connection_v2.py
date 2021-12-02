import sqlite3
con = sqlite3.connect('fgj_uniformes.db')
cur = con.cursor()



con.execute('''CREATE TABLE IF NOT EXISTS uniformes 
               (id integer primary key autoincrement,
               fecha text,
               num_empleado integer unique, 
               nombre text,
               email text not null,
               celular text not null,
               puesto text, 
               sexo text,
               municipio text,
               area_fiscalia_dist text,
               area_direccion_gral text,
               area_direccion text,
               area_jefatura text,
               area_comision text,
               talla text,
               confirmacion bool)''')
con.commit()
con.close()