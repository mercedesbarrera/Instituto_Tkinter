import customtkinter as ctk
from src.controllers.material_controller import MaterialController
from src.controllers.aula_controller import AulaController
from tkinter import filedialog
from tkinter import ttk, messagebox

class MaterialView(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.title("Gestión de Materiales")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.grab_set()
        self.lift()
        self.focus_force()

        # --- Frame de entradas y combos ---
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10, padx=10, fill="x")

        # Entradas
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre del material")
        self.entry_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.entry_cantidad = ctk.CTkEntry(form_frame, placeholder_text="Cantidad")
        self.entry_cantidad.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # ComboBox para seleccionar aula
        aulas = AulaController.obtener_todos()
        self.combo_aulas = ctk.CTkComboBox(form_frame, values=[f"{a.id} | {a.numero}" for a in aulas])
        self.combo_aulas.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Que las columnas 0,1,2 se estiren
        for i in range(3):
            form_frame.columnconfigure(i, weight=1)

        # --- Frame de botones ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10, padx=10, fill="x")

        btn_add = ctk.CTkButton(btn_frame, text="Añadir Material", command=self.add)
        btn_add.grid(row=0, column=0, padx=5)

        btn_importar = ctk.CTkButton(btn_frame, text="Importar desde CSV", command=self.importar_csv)
        btn_importar.grid(row=0, column=1, padx=5)

        btn_del = ctk.CTkButton(btn_frame, text="Borrar Material", command=self.delete)
        btn_del.grid(row=0, column=2, padx=5)

        # --- TreeView ---
        style = ttk.Style(self)
        style.configure("Treeview", font=("Arial", 14), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

        self.tree = ttk.Treeview(
            self,
            columns=("id", "nombre", "cantidad", "aula"),
            show="headings",
            height=8
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("aula", text="Aula")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("cantidad", width=80, anchor="center")

        self.tree.pack(pady=10, fill="both", expand=True)

        self.cargar()

    def cargar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for m in MaterialController.obtener_todos():
            self.tree.insert(
                "",
                "end",
                values=(m.id, m.nombre, m.cantidad, m.aula_numero)
            )

    def add(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()
        aula_text = self.combo_aulas.get()

        if not nombre or not cantidad.isdigit() or not aula_text:
            messagebox.showerror("Error", "Datos incorrectos")
            return

        aula_id = int(aula_text.split("|")[0].strip())
        MaterialController.crear(nombre, int(cantidad), aula_id)
        self.cargar()

    def delete(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un material")
            return

        valores = self.tree.item(seleccionado[0])["values"]
        material_id = valores[0]

        MaterialController.borrar(material_id)
        self.cargar()

    def cerrar(self):
        self.destroy()

    def importar_csv(self):
        archivo = filedialog.askopenfilename(
            title="Selecciona archivo CSV",
            filetypes=[("CSV files", "*.csv")]
        )

        if archivo:
            mensaje = MaterialController.importar_desde_csv(archivo)
            messagebox.showinfo("Importación", mensaje)
            self.cargar()
