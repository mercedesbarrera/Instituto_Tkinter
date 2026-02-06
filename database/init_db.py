import _sqlite3
from database.database import get_connection
from database import queries
#-----INICIALIZAR BASE DE DATOS-------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_ADMIN)
    cursor.execute(queries.CREATE_TABLE_ALUMNOS)
    cursor.execute(queries.CREATE_TABLE_PROFESORES)
    cursor.execute(queries.CREATE_TABLE_AULAS)
    cursor.execute(queries.CREATE_TABLE_ASIGNATURAS)
    cursor.execute(queries.CREATE_TABLE_MATERIAL)
    cursor.execute(queries.CREATE_TABLE_DIRECCION)
    cursor.execute(queries.CREATE_TABLE_CLASES)
    cursor.execute(queries.CREATE_TABLE_MATRICULAS)
    cursor.execute(queries.CREATE_TABLE_CONVOCATORIAS)
    cursor.execute(queries.INSERT_CONVOCATORIAS)
    cursor.execute(queries.CREATE_TABLE_CALIFICACIONES)

    conn.commit()
    conn.close()

    print("Base de datos creada correctamente")

if __name__ == "__main__":
    init_db()

