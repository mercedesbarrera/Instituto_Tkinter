import customtkinter as ctk
from src.controllers.login_controller import LoginController
from src.views.main_menu_view import MainMenuView


class LoginView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Login Instituto")
        self.geometry("400x300")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        #--- Formulario de login ---
        self.label = ctk.CTkLabel(self, text="Login")
        self.label.pack(pady=20)

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_pass.pack(pady=10)

        self.btn = ctk.CTkButton(self, text="Entrar", command=self.login)
        self.btn.pack(pady=20)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack()

#--- Funciones ---
    #--- Función para validar el login ---
    def login(self):

        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        ok = LoginController.validar_login(user, pwd)

        if ok:
            MainMenuView()
            self.withdraw()
        else:
            self.msg.configure(text="Usuario o password incorrecto")

    #--- Función para cerrar la ventana ---
    def cerrar(self):
        self.destroy()