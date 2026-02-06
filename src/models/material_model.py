class Material:
#---MODELO ATRIBUTO---
    def __init__(self, id, nombre, cantidad, aula_id, aula_numero=None):
        self.id=id
        self.nombre=nombre
        self.cantidad=cantidad
        self.aula_id=aula_id
        self.aula_numero=aula_numero # Para mostrar en la vista "aula 101"
