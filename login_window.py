import tkinter as tk
from tkinter import messagebox
from user_manager import UserManager
from main_window import MainWindow
from register_window import RegisterWindow

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Tkinder - Iniciar Sesión")
        self.master.geometry("300x200")

        self.user_manager = UserManager()

        tk.Label(master, text="Usuario").pack()
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        tk.Label(master, text="Contraseña").pack()
        self.entry_clave = tk.Entry(master, show="*")
        self.entry_clave.pack()

        tk.Button(master, text="Iniciar Sesión", command=self.iniciar_sesion).pack(pady=5)
        tk.Button(master, text="Registrarse", command=self.abrir_ventana_registro).pack()

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()

        if self.user_manager.verificar_login(usuario, clave):
            messagebox.showinfo("Bienvenido", f"Hola, {usuario}")
            self.master.destroy()
            es_admin = self.user_manager.es_admin(usuario)
            self.abrir_ventana_principal(usuario, es_admin)

        else:
            messagebox.showerror("Error", "Usuario o clave incorrecta")

    def abrir_ventana_principal(self, usuario, es_admin):
        ventana_principal = tk.Tk()

        if es_admin:
            from admin_window import AdminWindow
            AdminWindow(ventana_principal, usuario)
        else:
            from main_window import MainWindow
            MainWindow(ventana_principal, usuario)
        ventana_principal.mainloop()

    def abrir_ventana_registro(self):
        self.master.withdraw()  # Oculta la ventana actual
        ventana_registro = tk.Toplevel()
        RegisterWindow(ventana_registro, self.master)
