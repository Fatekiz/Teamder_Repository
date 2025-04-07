import tkinter as tk

class MainWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Tkinder - Buscar Equipos")
        self.master.geometry("400x300")

        label_bienvenida = tk.Label(master, text=f"¡Bienvenido a Tkinder, {usuario}!", font=("Arial", 14))
        label_bienvenida.pack(pady=20)

        # Aquí irán más elementos para buscar equipos o juegos
        label_info = tk.Label(master, text="(Aquí puedes buscar jugadores, crear grupo, etc...)")
        label_info.pack()
