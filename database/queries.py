#Crear tabla
CREATE_TABLE_ADMIN='''
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL 
        );
        '''

#-----------ADMINISTRADORES----------
INSERT_ADMIN='''
INSERT INTO admin (usuario, password)
VALUES (?,?);
'''

SELECT_ADMIN_LOGIN='''
SELECT id, usuario
from admin
WHERE usuario = ? AND password=?;
'''

##UPDATE Y DELETE
"""4️⃣ El patrón mental que debes usar 🧠

Apúntate esto:

Cada pantalla → solo necesita su propio CRUD mínimo

Ejemplo:

Login → INSERT + SELECT

Alta alumno → INSERT

Listado alumnos → SELECT

Editar alumno → UPDATE

Borrar alumno → DELETE

Nunca todo a la vez."""