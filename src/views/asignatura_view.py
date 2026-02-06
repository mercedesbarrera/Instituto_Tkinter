import customtkinter as ctk
from src.controllers.asignatura_controller import AsignaturaController
from tkinter import ttk
class AsignaturaView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.title("Gestión de Asignaturas")
        self.geometry("500x400")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()
        # --- Formulario de entrada ---
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre")
        self.entry_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.entry_departamento = ctk.CTkEntry(form_frame, placeholder_text="Departamento")
        self.entry_departamento.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        for i in range(2):
            form_frame.columnconfigure(i, weight=1)

        style= ttk.Style()
        style.configure(
            "Treeview",
            font=("Arial",14),
            rowheight=28
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 13, "bold")
        )


        # TreeView
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame, orientation="vertical")
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Nombre", "Departamento"),
            show="headings",
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Departamento", text="Departamento")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200)
        self.tree.column("Departamento", width=150)
        self.tree.pack(fill="both", expand=True)

        self.tree_scroll.configure(command=self.tree.yview)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_add = ctk.CTkButton(btn_frame, text="Añadir Asignatura", command=self.add)
        btn_add.grid(row=0, column=0, padx=5)

        btn_del = ctk.CTkButton(btn_frame, text="Borrar Asignatura", command=self.delete)
        btn_del.grid(row=0, column=1, padx=5)

        self.cargar()

    def cargar(self):
        # Limpiar TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Agregar asignaturas
        for a in AsignaturaController.obtener_todos():
            self.tree.insert("", "end", values=(a.id, a.nombre, a.departamento))

    def add(self):
        nombre = self.entry_nombre.get()
        departamento = self.entry_departamento.get()
        if nombre and departamento:
            AsignaturaController.crear(nombre, departamento)
            self.cargar()

    def delete(self):
        selected = self.tree.selection()
        if selected:
            asignatura_id = int(self.tree.item(selected[0])["values"][0])
            AsignaturaController.borrar(asignatura_id)
            self.cargar()

    def cerrar(self):
        self.destroy()