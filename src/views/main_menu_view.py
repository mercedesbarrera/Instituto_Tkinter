import customtkinter as ctk
from src.views.alumno_view import AlumnoView
from src.views.profesor_view import ProfesorView
from src.views.direccion_view import DireccionView
from src.views.aula_view import AulaView
from src.views.material_view import MaterialView
from src.views.asignatura_view import AsignaturaView
from src.views.clase_view import ClaseView
from src.views.matricula_view import MatriculaView
from src.views.calificacion_view import CalificacionView


class MainMenuView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Instituto - Menú Principal")
        self.geometry("700x600")
        self.configure(fg_color="#f0f0f0")  # Fondo claro

        # --- Título ---
        titulo = ctk.CTkLabel(
            self,
            text="Menú Principal",
            font=("Arial", 24, "bold"),
            text_color="#333"
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=30)

        # --- Botones ---
        botones = [
            ("Gestión Alumnos", AlumnoView),
            ("Gestión Profesores", ProfesorView),
            ("Dirección", DireccionView),
            ("Aulas", AulaView),
            ("Materiales", MaterialView),
            ("Asignaturas", AsignaturaView),
            ("Clases", ClaseView),
            ("Matrículas", MatriculaView),
            ("Calificaciones", CalificacionView)
        ]

        # Crear botones en 2 columnas
        for idx, (texto, vista) in enumerate(botones):
            row = 1 + idx // 2  # fila empezando desde 1 (después del título)
            col = idx % 2       # columna 0 o 1
            btn = ctk.CTkButton(
                self,
                text=texto,
                font=("Arial", 16),
                width=250,
                height=50,
                command=vista
            )
            btn.grid(row=row, column=col, padx=20, pady=15, sticky="nsew")

        # Que las columnas se estiren
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Botón Salir ---
        btn_salir = ctk.CTkButton(
            self,
            text="Salir",
            font=("Arial", 16),
            width=250,
            height=50,
            command=self.salir
        )
        btn_salir.grid(row=10, column=0, columnspan=2, pady=30)

    def salir(self):
        self.after(100, self._salida_limpia)

    def _salida_limpia(self):
        self.quit()
        self.destroy()
