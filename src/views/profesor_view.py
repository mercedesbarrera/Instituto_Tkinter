import customtkinter as ctk
from tkinter import ttk
from src.controllers.profesor_controller import ProfesorController


class ProfesorView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Gestión de Profesores")
        self.geometry("700x500")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()

        # --- Entradas ---
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre")
        self.entry_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.entry_apellidos = ctk.CTkEntry(form_frame, placeholder_text="Apellidos")
        self.entry_apellidos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.entry_dni = ctk.CTkEntry(form_frame, placeholder_text="DNI")
        self.entry_dni.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.entry_departamento = ctk.CTkEntry(form_frame, placeholder_text="Departamento")
        self.entry_departamento.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        for i in range(4):
            form_frame.columnconfigure(i, weight=1)

        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 14), rowheight=28)

        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

        # --- TreeView ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame, orientation="vertical")
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Nombre", "Apellidos", "DNI", "Departamento"),
            show="headings",
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse"
        )

        for col in ("ID", "Nombre", "Apellidos", "DNI", "Departamento"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=150)
        self.tree.column("Apellidos", width=150)
        self.tree.column("DNI", width=100)
        self.tree.column("Departamento", width=150)

        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.configure(command=self.tree.yview)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_add = ctk.CTkButton(btn_frame, text="Añadir Profesor", command=self.add)
        btn_add.grid(row=0,column=0,padx=5)

        btn_del = ctk.CTkButton(btn_frame, text="Borrar Seleccionado", command=self.delete)
        btn_del.grid(row=0,column=1,padx=5)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)

        self.cargar()

    def cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in ProfesorController.obtener_todos():
            self.tree.insert(
                "", "end",
                values=(p.id, p.nombre, p.apellidos, p.dni, p.departamento)
            )

    def add(self):
        ok, mensaje = ProfesorController.crear(
            self.entry_nombre.get(),
            self.entry_apellidos.get(),
            self.entry_dni.get(),
            self.entry_departamento.get()
        )
        self.msg.configure(text=mensaje)
        if ok:
            self.cargar()

    def delete(self):
        selected = self.tree.selection()
        if selected:
            profesor_id = self.tree.item(selected[0])["values"][0]
            ProfesorController.borrar(profesor_id)
            self.cargar()

    def cerrar(self):
        self.destroy()
