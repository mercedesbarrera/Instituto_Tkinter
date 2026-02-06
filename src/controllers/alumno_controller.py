import sqlite3

from database.database import get_connection
from src.models.alumno_model import Alumno


class AlumnoController:
#----CRUD PARA ALUMNOS-------
#- obtener_todos: Devuelve una lista de objetos Alumno con todos los alumnos registrados.
    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, apellidos, dni, fecha_nacimiento
            FROM alumnos
        """)

        rows = cursor.fetchall()
        conn.close()

        alumnos = []
        for r in rows:
            alumnos.append(Alumno(
                r["id"], r["nombre"], r["apellidos"],
                r["dni"], r["fecha_nacimiento"]
            ))

        return alumnos

#- crear: Inserta un nuevo alumno en la base de datos. Devuelve un mensaje de éxito o error.
    @staticmethod
    def crear(nombre, apellidos, dni, fecha):
        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO alumnos (nombre, apellidos, dni, fecha_nacimiento)
                VALUES (?, ?, ?, ?)
            """, (nombre, apellidos, dni, fecha))

            conn.commit()
            conn.close()
            return True, "Alumno insertado correctamente"

        except sqlite3.IntegrityError:
            return False, "El dni ya existe"

        finally:
            conn.close()

#- borrar: Elimina un alumno de la base de datos por su ID. Devuelve un mensaje de éxito o error.
    @staticmethod
    def borrar(alumno_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM alumnos WHERE id = ?",
            (alumno_id,)
        )

        conn.commit()
        conn.close()
#- editar: Actualiza los datos de un alumno existente. Devuelve un mensaje de éxito o error.
    @staticmethod
    def editar(alumno_id, nombre, apellidos, dni, fecha):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE alumnos
                SET nombre = ?, apellidos = ?, dni = ?, fecha_nacimiento = ?
                WHERE id = ?
            """, (nombre, apellidos, dni, fecha, alumno_id))
            conn.commit()
            return True, "Alumno actualizado correctamente"
        except sqlite3.IntegrityError:
            return False, "El DNI ya existe"
        finally:
            conn.close()
