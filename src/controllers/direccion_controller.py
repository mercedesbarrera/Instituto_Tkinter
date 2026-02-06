import sqlite3
from database.database import get_connection
from src.models.direccion_model import Direccion


class DireccionController:
#----CRUD PARA DIRECCION-------
#- obtener_todos: Devuelve una lista de objetos Direccion con todos los miembros de
# dirección registrados, incluyendo el nombre completo del profesor y su cargo.
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT d.id, d.profesor_id, p.nombre, p.apellidos, d.cargo
            FROM direccion d
            JOIN profesores p ON d.profesor_id = p.id
        """)

        rows = cursor.fetchall()
        conn.close()

        direcciones = []
        for r in rows:
            direcciones.append(
                Direccion(
                    r["id"],
                    r["profesor_id"],
                    r["nombre"],
                    r["apellidos"],
                    r["cargo"]
                )
            )
        return direcciones
#- crear: Inserta un nuevo miembro de dirección en la base de datos. Devuelve un mensaje de éxito o error.

    @staticmethod
    def crear(profesor_id, cargo):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO direccion (profesor_id, cargo)
                VALUES (?, ?)
            """, (profesor_id, cargo))

            conn.commit()
            return True, "Miembro de dirección añadido"

        except sqlite3.IntegrityError:
            return False, "Este profesor ya tiene un cargo"

        finally:
            conn.close()

#- borrar: Elimina un miembro de dirección de la base de datos por su ID. Devuelve un mensaje de éxito o error.
    @staticmethod
    def borrar(direccion_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM direccion WHERE id = ?",
            (direccion_id,)
        )

        conn.commit()
        conn.close()
