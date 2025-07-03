import tkinter as tk
from tkinter import ttk

# Importación de las ventanas de cada funcionalidad
from profile_window import ProfileWindow
from foro_window import ForoWindow
from salas_window import SalasWindow
from eventos_window import EventosWindow
from reportes_window import ReportesWindow
from mis_reportes_window import MisReportesWindow
from calendario_window import CalendarioWindow
from conexion_gamer_window import abrir_conexion_gamer
from team_crud import abrir_crud_equipos

class MainWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Teamder - Buscar Equipos")
        
        # Establecer un tamaño fijo para la ventana principal
        self.master.geometry("600x700")  # Dimensiones fijas
        self.master.minsize(600, 700)  # Tamaño mínimo de la ventana
        


        self.usuario = usuario

        # Título de bienvenida
        ttk.Label(master, text=f"🎮 ¡Bienvenido a Teamder, {usuario}!", font=("Arial", 14, "bold")).pack(pady=20)

        # === 🔧 Sección principal ===
        frame_principal = ttk.LabelFrame(master, text="Opciones principales", padding=(10, 5))
        frame_principal.pack(pady=10, fill="x", padx=20)

        ttk.Button(frame_principal, text="👤 Ajustes de Perfil", command=self.abrir_perfil).pack(fill="x", pady=5)
        ttk.Button(frame_principal, text="🎮 Conexión Gamer", command=self.abrir_conexion_gamer).pack(fill="x", pady=5)
        ttk.Button(frame_principal, text="💬 Acceder al Foro", command=self.abrir_foro).pack(fill="x", pady=5)

        # === 🎲 Otras funcionalidades ===
        frame_secundario = ttk.LabelFrame(master, text="Actividades", padding=(10, 5))
        frame_secundario.pack(pady=10, fill="x", padx=20)

        ttk.Button(frame_secundario, text="🕹️ Salas de Juego", command=self.abrir_salas).pack(fill="x", pady=5)
        ttk.Button(frame_secundario, text="📅 Eventos", command=self.abrir_eventos).pack(fill="x", pady=5)
        ttk.Button(frame_secundario, text="📆 Mi Calendario", command=self.abrir_calendario).pack(fill="x", pady=5)

        # === 💼 Equipos ===
        frame_equipos = ttk.LabelFrame(master, text="Equipos", padding=(10, 5))
        frame_equipos.pack(pady=10, fill="x", padx=20)

        ttk.Button(frame_equipos, text="⚙️ Gestionar Equipos", command=self.abrir_equipos).pack(fill="x", pady=5)

        # === 🛠️ Soporte ===
        frame_soporte = ttk.LabelFrame(master, text="Soporte", padding=(10, 5))
        frame_soporte.pack(pady=10, fill="x", padx=20)

        ttk.Button(frame_soporte, text="⚠️ Reportar Problema", command=self.abrir_reportes).pack(fill="x", pady=5)
        ttk.Button(frame_soporte, text="📝 Mis Reportes", command=self.abrir_mis_reportes).pack(fill="x", pady=5)

        # === 🚪 Salida === (Este botón estará al final)
        ttk.Button(master, text="🚪 Salir", command=master.quit, width=25).pack(pady=15)

        ttk.Label(master, text="(Aquí puedes buscar jugadores, crear grupo, etc...)").pack()

    # Funciones para abrir cada ventana
    def abrir_perfil(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        ProfileWindow(top, self.usuario)

    def abrir_foro(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        ForoWindow(top, self.usuario)

    def abrir_salas(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        SalasWindow(top, self.usuario)

    def abrir_eventos(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        EventosWindow(top, self.usuario)

    def abrir_reportes(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        ReportesWindow(top, self.usuario)

    def abrir_mis_reportes(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        MisReportesWindow(top, self.usuario)

    def abrir_calendario(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        CalendarioWindow(top, self.usuario)

    def abrir_conexion_gamer(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        abrir_conexion_gamer(top, self.usuario)

    def abrir_equipos(self):
        top = tk.Toplevel(self.master)
        top.geometry("600x400")
        top.resizable(False, False)  # Deshabilitar redimensionamiento
        abrir_crud_equipos(top, self.usuario)
