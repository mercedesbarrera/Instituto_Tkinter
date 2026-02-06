import customtkinter as ctk
from tkinter import ttk
from src.controllers.direccion_controller import DireccionController
from src.controllers.profesor_controller import ProfesorController

class DireccionView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Dirección del Centro")
        self.geometry("700x500")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()

        # --- Formulario superior ---
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Profesor
        self.profesores = ProfesorController.obtener_todos()
        self.combo_profesores = ctk.CTkComboBox(
            form_frame,
            values=[f"{p.id} - {p.nombre} {p.apellidos}" for p in self.profesores]
        )
        self.combo_profesores.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Cargo
        self.combo_cargo = ctk.CTkComboBox(
            form_frame,
            values=["Director", "Jefe de Estudios", "Secretario"]
        )
        self.combo_cargo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botón Añadir
        btn_add = ctk.CTkButton(form_frame, text="Asignar cargo", command=self.add)
        btn_add.grid(row=0, column=2, padx=5, pady=5)

        # Que las columnas 0 y 1 se estiren
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        # --- TreeView ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame, orientation="vertical")
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Profesor", "Cargo"),
            show="headings",
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse"
        )

        for col in ("ID", "Profesor", "Cargo"):
            self.tree.heading(col, text=col)

        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 14), rowheight=28)

        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Profesor", width=250)
        self.tree.column("Cargo", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.configure(command=self.tree.yview)

        # Botón borrar
        btn_del = ctk.CTkButton(self, text="Borrar cargo", command=self.delete)
        btn_del.pack(pady=10)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)

        self.cargar()

    # --- Cargar TreeView ---
    def cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for d in DireccionController.obtener_todos():
            self.tree.insert(
                "", "end",
                values=(d.id, f"{d.nombre} {d.apellidos}", d.cargo)
            )

    # --- Añadir dirección ---
    def add(self):
        profesor_id = self.combo_profesores.get().split("-")[0].strip()
        cargo = self.combo_cargo.get()

        ok, mensaje = DireccionController.crear(profesor_id, cargo)
        self.msg.configure(text=mensaje)
        if ok:
            self.cargar()

    # --- Borrar cargo ---
    def delete(self):
        selected = self.tree.selection()
        if selected:
            direccion_id = self.tree.item(selected[0])["values"][0]
            DireccionController.borrar(direccion_id)
            self.cargar()

    def cerrar(self):
        self.destroy()
