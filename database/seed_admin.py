from database.database import get_connection
from database.queries import INSERT_ADMIN

conn = get_connection()
cursor = conn.cursor()

cursor.execute(INSERT_ADMIN, ("admin", "1234"))

conn.commit()
conn.close()

print("Admin creado")
