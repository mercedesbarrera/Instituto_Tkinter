import customtkinter as ctk
from tkinter import ttk
from src.controllers.matricula_controller import MatriculaController
from src.controllers.alumno_controller import AlumnoController
from src.controllers.clase_controller import ClaseController

class MatriculaView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Gestión de Matrículas")
        self.geometry("700x500")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()

        # --- Frame de entradas y combos ---
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Combo Alumnos
        alumnos = AlumnoController.obtener_todos()
        self.combo_alumnos = ctk.CTkComboBox(
            form_frame,
            values=[f"{a.id} | {a.nombre} {a.apellidos}" for a in alumnos]
        )
        self.combo_alumnos.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Combo Clases
        clases = ClaseController.obtener_todas()
        self.combo_clases = ctk.CTkComboBox(
            form_frame,
            values=[f"{c['id']} | {c['asignatura']}" for c in clases]
        )
        self.combo_clases.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Año académico
        self.entry_anio = ctk.CTkEntry(form_frame, placeholder_text="Año académico")
        self.entry_anio.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Que todas las columnas se estiren
        for i in range(3):
            form_frame.columnconfigure(i, weight=1)

        # --- Frame de botón ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10, padx=10, fill="x")

        btn_add = ctk.CTkButton(btn_frame, text="Matricular alumno", command=self.add)
        btn_add.grid(row=0, column=0, padx=5)

        # --- TreeView ---
        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 14), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame, orientation="vertical")
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Alumno", "Asignatura", "Año académico"),
            show="headings",
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse",
            height=8
        )

        for col in ("ID", "Alumno", "Asignatura", "Año académico"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Alumno", width=200)
        self.tree.column("Asignatura", width=150)
        self.tree.column("Año académico", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.configure(command=self.tree.yview)

        # Mensaje
        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)

        self.cargar()


    # --- Cargar TreeView ---
    def cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for m in MatriculaController.obtener_todas():
            self.tree.insert(
                "", "end",
                values=(m['id'], m['alumno'], m['asignatura'], m['anio'])
            )

    # --- Añadir matrícula ---
    def add(self):
        alumno_id = int(self.combo_alumnos.get().split("|")[0].strip())
        clase_id = int(self.combo_clases.get().split("|")[0].strip())
        anio = self.entry_anio.get().strip()

        ok, mensaje = MatriculaController.crear(alumno_id, clase_id, anio)
        self.msg.configure(text=mensaje)

        if ok:
            self.cargar()

    def cerrar(self):
        self.destroy()
