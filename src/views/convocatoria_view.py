import customtkinter as ctk
from src.controllers.convocatoria_controller import ConvocatoriaController


class ConvocatoriaView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Convocatorias")
        self.geometry("300x300")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()

        #-- Frame de texto --
        self.text = ctk.CTkTextbox(self, width=250, height=200)
        self.text.pack(pady=10)

        for c in ConvocatoriaController.obtener_todas():
            self.text.insert("end", f"{c['id']} - {c['nombre']}\n")


    def cerrar(self):
        self.destroy()