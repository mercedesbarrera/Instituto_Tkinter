from database.database import get_connection
from database.queries import SELECT_ADMIN_LOGIN


class LoginController:
#----VALIDAR LOGIN-------
#- validar_login: Verifica si el usuario y contraseña proporcionados coinciden con un registro en la tabla de administradores.
# Devuelve True si las credenciales son válidas, de lo contrario False.
    @staticmethod
    def validar_login(usuario, password):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(SELECT_ADMIN_LOGIN, (usuario, password))
        row = cursor.fetchone()

        conn.close()

        return row is not None
