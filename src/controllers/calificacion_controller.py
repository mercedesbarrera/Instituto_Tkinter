import sqlite3
from database.database import get_connection
import csv
import os


class CalificacionController:
#----CRUD PARA CALIFICACIONES-------
#- obtener_por_matricula: Devuelve una lista de calificaciones para una matrícula específica.
    @staticmethod
    def obtener_por_matricula(matricula_id):
        conn = get_connection()
        cursor = conn.cursor()
        # Consulta para obtener las calificaciones junto con el nombre de la convocatoria
        cursor.execute("""
            SELECT convocatoria_id, nota
            FROM calificaciones
            WHERE matricula_id = ?
        """, (matricula_id,))

        filas = cursor.fetchall()
        conn.close()
        return filas

#- guardar: Inserta o actualiza una calificación para una matrícula y convocatoria específicas. Devuelve un mensaje de éxito o error.
    @staticmethod
    def guardar(matricula_id, convocatoria_id, nota):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Intentamos insertar la calificación. Si ya existe, se lanzará una excepción de integridad.
            cursor.execute("""
                INSERT INTO calificaciones (matricula_id, convocatoria_id, nota)
                VALUES (?, ?, ?)
            """, (matricula_id, convocatoria_id, nota))

            conn.commit()
            return True, "Nota guardada"

        except sqlite3.IntegrityError:
            # Si la calificación ya existe, actualizamos la nota.
            cursor.execute("""
                UPDATE calificaciones
                SET nota = ?
                WHERE matricula_id = ? AND convocatoria_id = ?
            """, (nota, matricula_id, convocatoria_id))

            conn.commit()
            return True, "Nota actualizada"

        finally:
            conn.close()
#- exportar_csv: Exporta las calificaciones de una asignatura y año específicos a un archivo CSV. Devuelve un mensaje de éxito o error.
    @staticmethod
    def exportar_csv(asignatura_id, anio):
        conn = get_connection()
        cursor = conn.cursor()
        # Consulta para obtener las calificaciones junto con el nombre del alumno, asignatura, convocatoria y año
        cursor.execute("""
            SELECT 
                a.apellidos || ', ' || a.nombre AS alumno,
                asig.nombre AS asignatura,
                c.nombre AS convocatoria,
                cal.nota,
                m.anio
            FROM calificaciones cal
            JOIN matriculas m ON cal.matricula_id = m.id
            JOIN alumnos a ON m.alumno_id = a.id
            JOIN clases cl ON m.clase_id = cl.id
            JOIN asignaturas asig ON cl.asignatura_id = asig.id
            JOIN convocatorias c ON cal.convocatoria_id = c.id
            WHERE asig.id = ? AND m.anio = ?
            ORDER BY a.apellidos, a.nombre
        """, (asignatura_id, anio))

        filas = cursor.fetchall()
        conn.close()

        if not filas:
            return False, "No hay calificaciones para exportar"

        nombre_archivo = f"calificaciones_{anio}.csv"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        # Escribir los datos en el archivo CSV
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Alumno", "Asignatura", "Convocatoria", "Nota", "Año"])

            for fila in filas:
                writer.writerow(fila)

        return True, f"Archivo exportado correctamente: {ruta}"
