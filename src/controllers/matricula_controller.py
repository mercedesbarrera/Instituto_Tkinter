import sqlite3
from database.database import get_connection

class MatriculaController:
#----CRUD PARA MATRICULAS-------
#- obtener_todas: Devuelve una lista de todas las matrículas registradas, incluyendo el nombre del alumno, la asignatura y el año.
    @staticmethod
    def obtener_todas():
        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
            SELECT 
                m.id,
                a.nombre || ' ' || a.apellidos AS alumno,
                asig.nombre AS asignatura,
                asig.id AS asignatura_id,
                m.anio
            FROM matriculas m
            JOIN alumnos a ON m.alumno_id = a.id
            JOIN clases c ON m.clase_id = c.id
            JOIN asignaturas asig ON c.asignatura_id = asig.id
        """)

        filas=cursor.fetchall()
        conn.close()
        return filas
#- crear: Inserta una nueva matrícula en la base de datos. Devuelve un mensaje de éxito o error.
    @staticmethod
    def crear(alumno_id, clase_id, anio):
        conn=get_connection()
        cursor=conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO matriculas (alumno_id, clase_id, anio)
                VALUES (?,?,?)
                """, (alumno_id,clase_id,anio))

            conn.commit()
            return True, "Matrícula creada correctamente"

        except sqlite3.IntegrityError:
            return False, "El alumno ya está matriculado en esa clase"

        finally:
            conn.close()


