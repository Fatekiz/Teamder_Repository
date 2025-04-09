import tkinter as tk
from tkinter import messagebox
from profile_window import ProfileWindow

class MainWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Tkinder - Buscar Equipos")
        self.master.geometry("600x500")

        self.usuario = usuario

        label_bienvenida = tk.Label(master, text=f"¡Bienvenido a Tkinder, {usuario}!", font=("Arial", 14))
        label_bienvenida.pack(pady=20)

        tk.Button(master, text="Ajustes de Perfil", command=self.abrir_perfil).pack(pady=10)

        # Aquí irán más elementos para buscar equipos o juegos
        label_info = tk.Label(master, text="(Aquí puedes buscar jugadores, crear grupo, etc...)")
        label_info.pack()

    def abrir_perfil(self):
        ProfileWindow(tk.Toplevel(self.master), self.usuario)
