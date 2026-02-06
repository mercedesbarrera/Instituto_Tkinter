import customtkinter as ctk
from src.controllers.aula_controller import AulaController
from tkinter import messagebox,ttk

class AulaView(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Aulas")
        self.geometry("500x400")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()
        # --- Formulario de entrada ---
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10, padx=10, fill="x")

        self.entry_numero=ctk.CTkEntry(form_frame,placeholder_text="Número")
        self.entry_numero.grid(row=0,column=0,padx=5,pady=5,sticky="ew")

        self.entry_capacidad=ctk.CTkEntry(form_frame, placeholder_text="Capacidad")
        self.entry_capacidad.grid(row=0,column=1,padx=5,pady=5,sticky="ew")

        btn_add = ctk.CTkButton(form_frame, text="Añadir Aula", command=self.add)
        btn_add.grid(row=0, column=2, padx=5, pady=5)

        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 14), rowheight=28)

        style.configure("Treeview.Heading", font=("Arial",16,"bold"))


        self.tree = ttk.Treeview(
            self,
            columns=("id", "numero", "capacidad"),
            show="headings",
            height=8
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("numero", text="Número")
        self.tree.heading("capacidad", text="Capacidad")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("capacidad", width=80, anchor="center")

        self.tree.pack(pady=10, fill="x")

        btn_del = ctk.CTkButton(self, text="Borrar Aula", command=self.delete)
        btn_del.pack(pady=5)

        self.cargar()

    def cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for a in AulaController.obtener_todos():
            self.tree.insert(
                "",
                "end",
                values=(a.id, a.numero, a.capacidad)
            )

    def add(self):
        numero = self.entry_numero.get()
        capacidad = self.entry_capacidad.get()

        if not numero or not capacidad.isdigit():
            messagebox.showerror("Error", "Datos incorrectos")
            return

        AulaController.crear(numero, int(capacidad))
        self.cargar()

    def delete(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un aula")
            return

        valores = self.tree.item(seleccionado[0])["values"]
        aula_id = valores[0]

        AulaController.borrar(aula_id)
        self.cargar()

    def cerrar(self):
        self.destroy()