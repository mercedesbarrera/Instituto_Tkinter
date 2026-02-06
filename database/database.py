import sqlite3

DB_NAME="database/app.db"
#----ESTABLECER CONEXION A LA BASE DE DATOS-------
def get_connection():
    conn= sqlite3.connect(DB_NAME)
    conn.row_factory=sqlite3.Row
    return conn