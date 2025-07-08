import tkinter as tk
from tkinter import messagebox

class AdminWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Tkinder Admin Panel")
        self.master.geometry("400x300")
        self.usuario = usuario
        tk.Label(master, text=f"Bienvenido, {usuario} (Admin)", font=("Arial", 14)).pack(pady=10)
        tk.Button(master, text="Ver todos los usuarios", command=self.ver_usuarios).pack(pady=5)
        tk.Button(master, text="Acceder al Foro", command=self.abrir_foro).pack(pady=5)
        tk.Button(master, text="Salas de Juego", command=self.abrir_salas).pack(pady=5)
        tk.Button(master, text="Gestionar Reportes", command=self.abrir_reportes).pack(pady=5)
        tk.Button(master, text="Gestionar Equipos", command=self.abrir_equipos).pack(pady=5)
        tk.Button(master, text="Gestionar Eventos", command=self.abrir_eventos).pack(pady=5)
        tk.Button(master, text="Cerrar", command=self.master.destroy).pack(pady=5)

    def ver_usuarios(self):
        try:
            with open("usuarios.json", "r") as f:
                import json
                usuarios = json.load(f)
            mensaje = "\n".join([f"{u} - {data['email']}" for u, data in usuarios.items()])
            messagebox.showinfo("Usuarios Registrados", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar usuarios: {e}")
            
    def abrir_foro(self):
        try:
            from foro_window import ForoWindow
            foro_window = tk.Toplevel(self.master)
            # Pasamos is_admin=True para darle privilegios de administrador en el foro
            ForoWindow(foro_window, self.usuario, is_admin=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el foro: {e}")
            
    def abrir_salas(self):
        try:
            from salas_window import SalasWindow
            salas_window = tk.Toplevel(self.master)
            # Pasamos is_admin=True para darle privilegios de administrador en las salas
            SalasWindow(salas_window, self.usuario, is_admin=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir las salas: {e}")
    
    def abrir_reportes(self):
        try:
            from reportes_admin_window import ReportesAdminWindow
            ventana = tk.Toplevel(self.master)
            ReportesAdminWindow(ventana)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir los reportes: {e}")

    def abrir_equipos(self):
        try:
            from team_crud import abrir_crud_equipos
            ventana = tk.Toplevel(self.master)
            abrir_crud_equipos(ventana, self.usuario)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la gestión de equipos: {e}")

    def abrir_eventos(self):
        try:
            from eventos_window import EventosWindow
            ventana = tk.Toplevel(self.master)
            EventosWindow(ventana, self.usuario, is_admin=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la gestión de eventos: {e}")
