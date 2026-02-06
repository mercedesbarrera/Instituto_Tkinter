from database.database import get_connection
from src.models.aula_model import Aula

class AulaController:
#----CRUD PARA AULAS-------
#- obtener_todos: Devuelve una lista de objetos Aula con todas las aulas registradas.
    @staticmethod
    def obtener_todos():
        conn= get_connection()
        cursor= conn.cursor()
        cursor.execute("SELECT * FROM aulas")
        filas= cursor.fetchall()
        conn.close()
        return [Aula(f['id'],f['numero'],f['capacidad']) for f in filas]
#- crear: Inserta una nueva aula en la base de datos. Devuelve un mensaje de éxito o error.
    @staticmethod
    def crear(numero,capacidad):
        conn=get_connection()
        cursor= conn.cursor()
        cursor.execute("INSERT INTO aulas (numero, capacidad) VALUES (?,?)", (numero,capacidad))
        conn.commit()
        conn.close()
#- borrar: Elimina un aula de la base de datos por su ID. Devuelve un mensaje de éxito o error.
    @staticmethod
    def borrar(aula_id):
        conn=get_connection()
        cursor= conn.cursor()
        cursor.execute("DELETE FROM aulas WHERE id = ?", (aula_id,))
        conn.commit()
        conn.close()