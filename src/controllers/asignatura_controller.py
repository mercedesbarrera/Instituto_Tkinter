from database.database import get_connection
from src.models.asignatura_model import Asignatura

class AsignaturaController:
#----CRUD PARA ASIGNATURAS-------
#- obtener_todos: Devuelve una lista de objetos Asignatura con todas las asignaturas registradas.
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM asignaturas")
        filas = cursor.fetchall()
        conn.close()
        return [Asignatura(f['id'], f['nombre'], f['departamento']) for f in filas]
#- crear: Inserta una nueva asignatura en la base de datos. Devuelve un mensaje de éxito o error.
    @staticmethod
    def crear(nombre, departamento):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO asignaturas (nombre, departamento) VALUES (?, ?)",
            (nombre, departamento)
        )
        conn.commit()
        conn.close()
#- borrar: Elimina una asignatura de la base de datos por su ID. Devuelve un mensaje de éxito o error.
    @staticmethod
    def borrar(asignatura_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM asignaturas WHERE id = ?", (asignatura_id,))
        conn.commit()
        conn.close()
