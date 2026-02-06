
import sqlite3
from database.database import get_connection
from src.models.clase_model import Clase

class ClaseController:
#----CRUD PARA CLASES-------
#- obtener_todos: Devuelve una lista de objetos Clase con todas las clases registradas

    @staticmethod
    def obtener_todas():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id,
                   p.nombre || ' ' || p.apellidos AS profesor,
                   a.nombre AS asignatura,
                   au.numero AS aula,
                   c.anio_academico
            FROM clases c
            JOIN profesores p ON c.profesor_id = p.id
            JOIN asignaturas a ON c.asignatura_id = a.id
            JOIN aulas au ON c.aula_id = au.id
        """)
        return cursor.fetchall()

#- crear: Inserta una nueva clase en la base de datos. Devuelve un mensaje de éxito o error.
    @staticmethod
    def crear(profesor_id, asignatura_id, aula_id, anio):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clases (profesor_id, asignatura_id, aula_id, anio_academico)
            VALUES (?, ?, ?, ?)
        """, (profesor_id, asignatura_id, aula_id, anio))

        conn.commit()
        conn.close()




