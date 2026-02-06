from database.database import get_connection


class ConvocatoriaController:
#----CRUD PARA CONVOCATORIAS-------
#- obtener_todas: Devuelve una lista de todas las convocatorias registradas en la base de datos.
    @staticmethod
    def obtener_todas():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM convocatorias")
        filas = cursor.fetchall()

        conn.close()
        return filas
