import customtkinter as ctk
from src.controllers.matricula_controller import MatriculaController
from src.controllers.convocatoria_controller import ConvocatoriaController
from src.controllers.calificacion_controller import CalificacionController


class CalificacionView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Calificaciones")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()


        # --- Matrículas ---
        self.matriculas = MatriculaController.obtener_todas()
        self.index = 0

        self.label_matricula = ctk.CTkLabel(self, text="")
        self.label_matricula.pack(pady=5)

        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(pady=5)

        ctk.CTkButton(nav, text="◀ Anterior", command=self.prev).pack(side="left", padx=5)
        ctk.CTkButton(nav, text="Siguiente ▶", command=self.next).pack(side="left", padx=5)

        # --- Convocatorias ---
        self.frame_notas = ctk.CTkFrame(self)
        self.frame_notas.pack(pady=10)

        btn_exportar = ctk.CTkButton(self, text="Exportar a CSV", command=self.exportar_csv)
        btn_exportar.pack(pady=10)
        self.inputs = {}

        for conv in ConvocatoriaController.obtener_todas():
            fila = ctk.CTkFrame(self.frame_notas)
            fila.pack(pady=3)

            ctk.CTkLabel(fila, text=conv['nombre'], width=120).pack(side="left")

            entry = ctk.CTkEntry(fila, width=80)
            entry.pack(side="left", padx=5)

            btn = ctk.CTkButton(
                fila,
                text="Guardar",
                command=lambda c=conv['id'], e=entry: self.guardar(c, e)
            )
            btn.pack(side="left")

            self.inputs[conv['id']] = entry

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=5)

        self.cargar_matricula()


    def cargar_matricula(self):
        if not self.matriculas:
            self.label_matricula.configure(text="No hay matrículas")
            return

        m = self.matriculas[self.index]
        self.matricula_id = m['id']

        self.label_matricula.configure(
            text=f"{m['alumno']} | {m['asignatura']} | {m['anio']}"
        )

        for e in self.inputs.values():
            e.delete(0, "end")

        for c in CalificacionController.obtener_por_matricula(self.matricula_id):
            convocatoria_id = c['convocatoria_id']

            if convocatoria_id in self.inputs:
                self.inputs[convocatoria_id].insert(0, str(c['nota']))


    def guardar(self, convocatoria_id, entry):
        try:
            nota = float(entry.get())
        except ValueError:
            self.msg.configure(text="Nota inválida")
            return

        ok, mensaje = CalificacionController.guardar(
            self.matricula_id,
            convocatoria_id,
            nota
        )
        self.msg.configure(text=mensaje)


    def prev(self):
        if self.index > 0:
            self.index -= 1
            self.cargar_matricula()


    def next(self):
        if self.index < len(self.matriculas) - 1:
            self.index += 1
            self.cargar_matricula()


    def cerrar(self):
        self.destroy()


    def exportar_csv(self):
        if not self.matriculas:
            self.msg.configure(text="No hay matrículas para exportar")
            return

        m=self.matriculas[self.index]

        ok,mensaje= CalificacionController.exportar_csv(
            asignatura_id=m['asignatura_id'],
            anio=m['anio'])


        self.msg.configure(text=mensaje)
