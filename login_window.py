import tkinter as tk 
from tkinter import messagebox  # Mostrar ventanas emergentes
from user_manager import UserManager  # Manejador de usuarios (verificación, tipo, etc.)
from main_window import MainWindow  # Ventana principal del usuario estándar
from register_window import RegisterWindow

class LoginWindow:
    def __init__(self, master):
        self.master = master  # Ventana principal (root)
        self.master.title("Teamder - Iniciar Sesión")  # Título de la ventana
        self.master.geometry("300x200")  # Tamaño de la ventana

        self.user_manager = UserManager()  # Instanciar UserManager

        # Etiqueta y campo para el nombre de usuario
        tk.Label(master, text="Usuario").pack()
        self.entry_usuario = tk.Entry(master)
        self.entry_usuario.pack()

        # Etiqueta y campo para la contraseña
        tk.Label(master, text="Contraseña").pack()
        self.entry_clave = tk.Entry(master, show="*")
        self.entry_clave.pack()

        # Botón para iniciar sesión y para entrar a la ventana de Registro
        tk.Button(master, text="Iniciar Sesión", command=self.iniciar_sesion).pack(pady=5)
    
        tk.Button(master, text="Registrarse", command=self.abrir_ventana_registro).pack()

    def iniciar_sesion(self):
        # Obtiene el nombre de usuario y clave ingresados
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()

        # Verifica las credenciales
        if self.user_manager.verificar_login(usuario, clave):
            # Si son correctas, muestra mensaje de bienvenida
            messagebox.showinfo("Bienvenido", f"Hola, {usuario}")
            self.master.destroy()  # Cierra la ventana de login
            

            es_admin = self.user_manager.es_admin(usuario)  # Verifica si el usuario es admin
            self.abrir_ventana_principal(usuario, es_admin)  # Abre la ventana correspondiente
        else:
            # Si son incorrectas, muestra mensaje de error
            messagebox.showerror("Error", "Usuario o clave incorrecta")

    def abrir_ventana_principal(self, usuario, es_admin):
        ventana_principal = tk.Tk()  # Crea una nueva ventana

        if es_admin:
            from admin_window import AdminWindow  # Se importa aquí para evitar importaciones innecesarias
            AdminWindow(ventana_principal, usuario)  # Abre la ventana de admin
        else:
            from main_window import MainWindow  # Para usuarios estándar
            MainWindow(ventana_principal, usuario)  # Abre la ventana principal
        ventana_principal.mainloop()  # Mantiene la ventana abierta

    def abrir_ventana_registro(self):
        self.master.withdraw()  # Oculta la ventana de login
        ventana_registro = tk.Toplevel()  # Crea una nueva ventana secundaria
        RegisterWindow(ventana_registro, self.master)  # Abre la ventana de registro con referencia a la original