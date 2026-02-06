import csv
from database.database import get_connection
from src.models.material_model import Material


class MaterialController:

#----CRUD PARA MATERIALES-------
#- obtener_todos: Devuelve una lista de objetos Material con todos los materiales registrados.
    @staticmethod
    def obtener_todos():
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("""
            SELECT m.id, m.nombre, m.cantidad, m.aula_id, a.numero as aula_numero
                       FROM materiales m
                       LEFT JOIN aulas a ON m.aula_id = a.id
        """)

        filas=cursor.fetchall()
        conn.close()
        return [Material(f['id'],f['nombre'],f['cantidad'],f['aula_id'],f['aula_numero']) for f in filas]

#- crear: Inserta un nuevo material en la base de datos. Devuelve un mensaje de éxito o error.
    @staticmethod
    def crear(nombre, cantidad, aula_id):
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO materiales (nombre, cantidad, aula_id) VALUES (?,?,?)",(nombre, cantidad, aula_id))
        conn.commit()
        conn.close()
#- borrar: Elimina un material de la base de datos por su ID. Devuelve un mensaje de éxito o error.
    @staticmethod
    def borrar(material_id):
        conn= get_connection()
        cursor= conn.cursor()
        cursor.execute("DELETE FROM materiales WHERE id= ?",(material_id,))
        conn.commit()
        conn.close()
#- importar_desde_csv: Importa materiales desde un archivo CSV. Devuelve un mensaje de éxito o error.
    @staticmethod
    def importar_desde_csv(archivo_csv):
        """
        Importa materiales desde un CSV.
        Columnas esperadas: nombre_material, cantidad, aula_id
        """
        conn = get_connection()
        cursor = conn.cursor()
        importados = 0
        errores = []
        # Validaciones:
        # - El archivo debe existir y ser legible.
        # - Cada fila debe tener nombre_material, cantidad y aula_id.
        # - cantidad y aula_id deben ser números.
        try:
            with open(archivo_csv, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                print("CABECERAS CSV:", reader.fieldnames)
                for fila in reader:
                    print("FILA:", fila)
                    nombre = fila.get("nombre_material") or fila.get("nombre")
                    cantidad = fila.get("cantidad")
                    aula_id = fila.get("aula_id") or fila.get("aula")

                    # Validaciones
                    if not nombre or not cantidad or not aula_id:
                        errores.append(f"Fila incompleta: {fila}")
                        continue

                    try:
                        cantidad = int(cantidad)
                        aula_id = int(aula_id)
                    except ValueError:
                        errores.append(f"Cantidad o aula_id no es número: {fila}")
                        continue

                    # Comprobar que el aula existe
                    cursor.execute("SELECT id FROM aulas WHERE id = ?", (aula_id,))
                    if not cursor.fetchone():
                        errores.append(f"Aula {aula_id} no existe: {fila}")
                        continue

                    # Insertar material
                    cursor.execute(
                        "INSERT INTO materiales (nombre, cantidad, aula_id) VALUES (?, ?, ?)",
                        (nombre, cantidad, aula_id)
                    )
                    importados += 1

            conn.commit()
        except FileNotFoundError:
            errores.append("Archivo no encontrado")
        except Exception as e:
            errores.append(str(e))
        finally:

            conn.close()

        mensaje = f"{importados} materiales importados correctamente."
        if errores:
            mensaje += "\nErrores:\n" + "\n".join(errores)
        return mensaje