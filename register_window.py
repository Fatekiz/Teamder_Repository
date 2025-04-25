import tkinter as tk
from tkinter import messagebox  # Para mostrar mensajes emergentes
from user_manager import UserManager  # Clase encargada de manejar usuarios

class RegisterWindow:
    def __init__(self, master, login_window):
        self.master = master  # Ventana actual (de registro)
        self.login_window = login_window  # Referencia a la ventana de login (para volver)
        self.master.title("Teamder - Registro")  # Título de la ventana
        self.master.geometry("300x250")  # Tamaño de la ventana

        self.user_manager = UserManager()  # Instancia del manejador de usuarios

        # Campo para el nombre de usuario
        tk.Label(master, text="Usuario").pack()
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        # Campo para el correo electrónico
        tk.Label(master, text="Email").pack()
        self.entry_email = tk.Entry(master)
        self.entry_email.pack()

        # Campo para la contraseña (oculta con "*")
        tk.Label(master, text="Contraseña").pack()
        self.entry_clave = tk.Entry(master, show="*")
        self.entry_clave.pack()

        # Botón para registrar al usuario
        tk.Button(master, text="Registrarse", command=self.registrar).pack(pady=5)
        # Botón para volver a la ventana de login
        tk.Button(master, text="Volver", command=self.volver_login).pack()

    def registrar(self):
        # Obtiene los valores ingresados por el usuario
        usuario = self.entry_usuario.get()
        email = self.entry_email.get()
        clave = self.entry_clave.get()

        # Llama a la función de registro en UserManager
        resultado = self.user_manager.registrar(usuario, email, clave)

        if resultado == "OK":
            # Si el registro fue exitoso, muestra un mensaje y vuelve al login
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.volver_login()
        else:
            # Si hubo un error (usuario ya existe, campos vacíos, etc.)
            messagebox.showwarning("Error", resultado)

    def volver_login(self):
        self.master.destroy()  # Cierra la ventana de registro
        self.login_window.deiconify()  # Muestra nuevamente la ventana de login