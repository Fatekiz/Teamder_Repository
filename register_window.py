import tkinter as tk
from tkinter import messagebox
from user_manager import UserManager

class RegisterWindow:
    def __init__(self, master, login_window):
        self.master = master
        self.login_window = login_window
        self.master.title("Tkinder - Registro")
        self.master.geometry("300x250")

        self.user_manager = UserManager()

        tk.Label(master, text="Usuario").pack()
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        tk.Label(master, text="Email").pack()
        self.entry_email = tk.Entry(master)
        self.entry_email.pack()

        tk.Label(master, text="Contraseña").pack()
        self.entry_clave = tk.Entry(master, show="*")
        self.entry_clave.pack()

        tk.Button(master, text="Registrarse", command=self.registrar).pack(pady=5)
        tk.Button(master, text="Volver", command=self.volver_login).pack()

    def registrar(self):
        usuario = self.entry_usuario.get()
        email = self.entry_email.get()
        clave = self.entry_clave.get()

        resultado = self.user_manager.registrar(usuario, email, clave)

        if resultado == "OK":
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.volver_login()
        else:
            messagebox.showwarning("Error", resultado)

    def volver_login(self):
        self.master.destroy()
        self.login_window.deiconify()  # Muestra la ventana de login
