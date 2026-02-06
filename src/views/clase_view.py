import customtkinter as ctk
from tkinter import ttk
from src.controllers.clase_controller import ClaseController
from src.controllers.profesor_controller import ProfesorController
from src.controllers.asignatura_controller import AsignaturaController
from src.controllers.aula_controller import AulaController

class ClaseView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Gestión de Clases")
        self.geometry("600x500")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()

        # --- Etiqueta ---
        self.label = ctk.CTkLabel(self, text="Crear Clase")
        self.label.pack(pady=10)

        # --- Frame de entradas y combos ---
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Combo Profesor
        self.combo_profesores = ctk.CTkComboBox(form_frame, values=[])
        self.combo_profesores.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Combo Asignatura
        self.combo_asignaturas = ctk.CTkComboBox(form_frame, values=[])
        self.combo_asignaturas.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Combo Aula
        self.combo_aulas = ctk.CTkComboBox(form_frame, values=[])
        self.combo_aulas.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Año académico
        self.entry_anio = ctk.CTkEntry(form_frame, placeholder_text="Año académico (ej. 2024-2025)")
        self.entry_anio.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Que todas las columnas se estiren
        for i in range(4):
            form_frame.columnconfigure(i, weight=1)

        # --- Frame de botón ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10, padx=10, fill="x")

        self.btn_add = ctk.CTkButton(btn_frame, text="Añadir Clase", command=self.add)
        self.btn_add.grid(row=0, column=0, padx=5)

        # --- TreeView ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame, orientation="vertical")
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Profesor", "Asignatura", "Aula", "Año académico"),
            show="headings",
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse",
            height=8
        )

        for col in ("ID", "Profesor", "Asignatura", "Aula", "Año académico"):
            self.tree.heading(col, text=col)

        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 14), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Profesor", width=150)
        self.tree.column("Asignatura", width=120)
        self.tree.column("Aula", width=80, anchor="center")
        self.tree.column("Año académico", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.configure(command=self.tree.yview)

        # Cargar combos y listado
        self.cargar_combos()
        self.cargar()

    # --- Cargar combos ---
    def cargar_combos(self):
        # Profesores
        profesores = ProfesorController.obtener_todos()
        prof_vals = [f"{p.id} | {p.nombre} {p.apellidos}" for p in profesores]
        self.combo_profesores.configure(values=prof_vals)
        if prof_vals:
            self.combo_profesores.set(prof_vals[0])

        # Asignaturas
        asignaturas = AsignaturaController.obtener_todos()
        asig_vals = [f"{a.id} | {a.nombre}" for a in asignaturas]
        self.combo_asignaturas.configure(values=asig_vals)
        if asig_vals:
            self.combo_asignaturas.set(asig_vals[0])

        # Aulas
        aulas = AulaController.obtener_todos()
        aulas_vals = [f"{a.id} | {a.numero}" for a in aulas]
        self.combo_aulas.configure(values=aulas_vals)
        if aulas_vals:
            self.combo_aulas.set(aulas_vals[0])

    # --- Cargar TreeView ---
    def cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for c in ClaseController.obtener_todas():
            self.tree.insert(
                "", "end",
                values=(c['id'], c['profesor'], c['asignatura'], f"Aula {c['aula']}", c['anio_academico'])
            )

    # --- Añadir clase ---
    def add(self):
        prof_text = self.combo_profesores.get()
        profesor_id = int(prof_text.split("|")[0].strip())

        asig_text = self.combo_asignaturas.get()
        asignatura_id = int(asig_text.split("|")[0].strip())

        aula_text = self.combo_aulas.get()
        aula_id = int(aula_text.split("|")[0].strip())

        anio = self.entry_anio.get().strip()
        if not anio:
            return  # Podrías mostrar un mensaje de error aquí

        ClaseController.crear(profesor_id, asignatura_id, aula_id, anio)
        self.cargar()

    def cerrar(self):
        self.destroy()
