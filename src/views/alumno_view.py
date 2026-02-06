import customtkinter as ctk
from tkinter import ttk
from src.controllers.alumno_controller import AlumnoController

class AlumnoView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.grab_set()
        self.lift()
        self.focus_force()

        self.title("Gestión de Alumnos")
        self.geometry("700x500")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        # --- Formulario ---
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=10, fill="x")

        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre")
        self.entry_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.entry_apellidos = ctk.CTkEntry(form_frame, placeholder_text="Apellidos")
        self.entry_apellidos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.entry_dni = ctk.CTkEntry(form_frame, placeholder_text="DNI")
        self.entry_dni.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.entry_fecha = ctk.CTkEntry(form_frame, placeholder_text="Fecha nacimiento")
        self.entry_fecha.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Hacer que se estiren bien
        for i in range(4):
            form_frame.columnconfigure(i, weight=1)


        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)

        #Estilos TreeView
        style = ttk.Style()
        style.configure(
            "Treeview",
            font=("Arial", 14),  # tamaño de letra filas
            rowheight=28  # altura de fila (muy importante)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 16, "bold")  # tamaño encabezados
        )
        # --- TreeView ---
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame, orientation="vertical")
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Nombre", "Apellidos", "DNI", "Fecha Nacimiento"),
            show="headings",
            yscrollcommand=self.tree_scroll.set,
            selectmode="browse"
        )

        # Encabezados
        for col in ("ID", "Nombre", "Apellidos", "DNI", "Fecha Nacimiento"):
            self.tree.heading(col, text=col)

        # Columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=150)
        self.tree.column("Apellidos", width=150)
        self.tree.column("DNI", width=100)
        self.tree.column("Fecha Nacimiento", width=120)

        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.configure(command=self.tree.yview)

        # --- Botones ---

        btn_frame=ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_add = ctk.CTkButton(btn_frame, text="Añadir Alumno", command=self.add)
        btn_add.grid(row=0, column=0, padx=10)

        btn_del = ctk.CTkButton(btn_frame, text="Borrar Seleccionado", command=self.delete)
        btn_del.grid(row=0, column=1, padx=10)

        btn_edit = ctk.CTkButton(btn_frame, text="Editar Seleccionado", command=self.edit)
        btn_edit.grid(row=0, column=2, padx=10)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)

        self.cargar()

    # --- Métodos ---
    def cargar(self):
        # Limpiar TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar alumnos
        for a in AlumnoController.obtener_todos():
            self.tree.insert(
                "", "end",
                values=(a.id, a.nombre, a.apellidos, a.dni, a.fecha_nacimiento)
            )

    def add(self):
        ok, mensaje = AlumnoController.crear(
            self.entry_nombre.get(),
            self.entry_apellidos.get(),
            self.entry_dni.get(),
            self.entry_fecha.get()
        )
        self.msg.configure(text=mensaje)
        if ok:
            self.cargar()

    def delete(self):
        selected = self.tree.selection()
        if selected:
            alumno_id = self.tree.item(selected[0])["values"][0]
            AlumnoController.borrar(alumno_id)
            self.cargar()

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            self.msg.configure(text="Selecciona un alumno")
            return

        alumno_id = self.tree.item(selected[0])["values"][0]
        nombre = self.entry_nombre.get()
        apellidos = self.entry_apellidos.get()
        dni = self.entry_dni.get()
        fecha = self.entry_fecha.get()

        ok, mensaje = AlumnoController.editar(alumno_id, nombre, apellidos, dni, fecha)
        self.msg.configure(text=mensaje)
        if ok:
            self.cargar()

    def cerrar(self):
        self.destroy()
