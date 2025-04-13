#juegos_window.py en este archivo se maneja la interfaz grafica de tkinter para gestionar los jeugos 
import tkinter as tk
from tkinter import messagebox
from game_manager import GameManager

class JuegosWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Juegos")
        self.master.geometry("400x300")

        self.game_manager = GameManager()

        # Lista de juegos
        self.lista_juegos = tk.Listbox(master)
        self.lista_juegos.pack(pady=20)
        self.cargar_juegos()

        # Botones para agregar, editar y eliminar juegos
        tk.Button(master, text="Agregar Juego", command=self.agregar_juego).pack(pady=5)
        tk.Button(master, text="Editar Juego", command=self.editar_juego).pack(pady=5)
        tk.Button(master, text="Eliminar Juego", command=self.eliminar_juego).pack(pady=5)

    def cargar_juegos(self):
        # Carga los juegos existentes en la lista
        juegos = self.game_manager.cargar_juegos()
        self.lista_juegos.delete(0, tk.END)  # Limpiar lista actual
        for juego in juegos:
            self.lista_juegos.insert(tk.END, juego)

    def agregar_juego(self):
        # Ventana para agregar un juego
        self.agregar_window = tk.Toplevel(self.master)
        self.agregar_window.geometry("300x200")
        self.agregar_window.title("Agregar Juego")

        tk.Label(self.agregar_window, text="Nombre del Juego").pack(pady=5)
        self.entry_nombre = tk.Entry(self.agregar_window)
        self.entry_nombre.pack(pady=5)

        tk.Label(self.agregar_window, text="Descripción del Juego").pack(pady=5)
        self.entry_descripcion = tk.Entry(self.agregar_window)
        self.entry_descripcion.pack(pady=5)

        tk.Button(self.agregar_window, text="Agregar", command=self.guardar_juego).pack(pady=5)

    def guardar_juego(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()

        resultado = self.game_manager.agregar_juego(nombre, descripcion)
        messagebox.showinfo("Resultado", resultado)

        self.agregar_window.destroy()
        self.cargar_juegos()

    def editar_juego(self):
        # Ventana para editar el juego seleccionado
        seleccionado = self.lista_juegos.curselection()
        if seleccionado:
            nombre_juego = self.lista_juegos.get(seleccionado[0])
            self.editar_window = tk.Toplevel(self.master)
            self.editar_window.geometry("300x200")
            self.editar_window.title(f"Editar {nombre_juego}")

            tk.Label(self.editar_window, text="Nueva Descripción").pack(pady=5)
            self.entry_nueva_descripcion = tk.Entry(self.editar_window)
            self.entry_nueva_descripcion.pack(pady=5)

            tk.Button(self.editar_window, text="Guardar Cambios", command=lambda: self.guardar_cambios(nombre_juego)).pack(pady=5)

    def guardar_cambios(self, nombre_juego):
        nueva_descripcion = self.entry_nueva_descripcion.get()
        resultado = self.game_manager.editar_juego(nombre_juego, nueva_descripcion)
        messagebox.showinfo("Resultado", resultado)

        self.editar_window.destroy()
        self.cargar_juegos()

    def eliminar_juego(self):
        # Ventana para eliminar un juego
        seleccionado = self.lista_juegos.curselection()
        if seleccionado:
            nombre_juego = self.lista_juegos.get(seleccionado[0])
            resultado = self.game_manager.eliminar_juego(nombre_juego)
            messagebox.showinfo("Resultado", resultado)

            self.cargar_juegos()
