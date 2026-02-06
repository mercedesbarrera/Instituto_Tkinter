import sqlite3
from database.database import get_connection
from src.models.profesor_model import Profesor


class ProfesorController:
#----CRUD PARA PROFESORES-------
#- obtener_todos: Devuelve una lista de objetos Profesor con todos los profesores registrados.
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, apellidos, dni, departamento
            FROM profesores
        """)

        rows = cursor.fetchall()
        conn.close()

        profesores = []
        for r in rows:
            profesores.append(
                Profesor(
                    r["id"],
                    r["nombre"],
                    r["apellidos"],
                    r["dni"],
                    r["departamento"]
                )
            )
        return profesores

#- crear: Inserta un nuevo profesor en la base de datos. Devuelve un mensaje de éxito o error.
    @staticmethod
    def crear(nombre, apellidos, dni, departamento):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO profesores (nombre, apellidos, dni, departamento)
                VALUES (?, ?, ?, ?)
            """, (nombre, apellidos, dni, departamento))

            conn.commit()
            return True, "Profesor creado correctamente"

        except sqlite3.IntegrityError:
            return False, "El DNI ya existe"

        finally:
            conn.close()


    @staticmethod
    def borrar(profesor_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM profesores WHERE id = ?",
            (profesor_id,)
        )

        conn.commit()
        conn.close()
