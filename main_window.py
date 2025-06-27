import tkinter as tk
from tkinter import messagebox
from profile_window import ProfileWindow
from foro_window import ForoWindow
from salas_window import SalasWindow
from eventos_window import EventosWindow
from reportes_window import ReportesWindow
from mis_reportes_window import MisReportesWindow
from calendario_window import CalendarioWindow
from conexion_gamer_window import abrir_conexion_gamer


class MainWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Teamder - Buscar Equipos")
        self.master.geometry("600x500")
        


        self.usuario = usuario

        label_bienvenida = tk.Label(master, text=f"¡Bienvenido a Teamder, {usuario}!", font=("Arial", 14))
        label_bienvenida.pack(pady=20)


        tk.Button(master, text="Acceder al Foro", command=self.abrir_foro).pack(pady=10)
        tk.Button(master, text="🎮 Conexión Gamer", command=self.abrir_conexion_gamer).pack(pady=10)
        tk.Button(master, text="Salas de Juego", command=self.abrir_salas).pack(pady=10)
        tk.Button(master, text="Eventos", command=self.abrir_eventos).pack(pady=10)
        tk.Button(master, text="Mi Calendario", command=self.abrir_calendario).pack(pady=10)
        tk.Button(master, text="Ajustes de Perfil", command=self.abrir_perfil).pack(pady=10)
        tk.Button(master, text="Reportar Problema", command=self.abrir_reportes).pack(pady=10)
        tk.Button(master, text="Mis Reportes", command=self.abrir_mis_reportes).pack(pady=5)
        
        


        tk.Button(master, text="Salir", command=master.quit).pack(pady=10)
        
        # Aquí irán más elementos para buscar equipos o juegos
        label_info = tk.Label(master, text="(Aquí puedes buscar jugadores, crear grupo, etc...)")
        label_info.pack()

    def abrir_perfil(self):
        ProfileWindow(tk.Toplevel(self.master), self.usuario)
        
    def abrir_foro(self):
        ForoWindow(tk.Toplevel(self.master), self.usuario)
        
    def abrir_salas(self):
        SalasWindow(tk.Toplevel(self.master), self.usuario)

    def abrir_eventos(self):
        EventosWindow(tk.Toplevel(self.master), self.usuario)
    
    def abrir_reportes(self):
        ReportesWindow(tk.Toplevel(self.master), self.usuario)
    
    def abrir_mis_reportes(self):
        MisReportesWindow(tk.Toplevel(self.master), self.usuario)

    def abrir_calendario(self):
        CalendarioWindow(tk.Toplevel(self.master), self.usuario)
    
    def abrir_conexion_gamer(self):
        abrir_conexion_gamer(self.master, self.usuario)


