import tkinter as tk
import json
import os

class MisReportesWindow:
    """
    Ventana para mostrar los reportes enviados por el usuario actual.
    """

    def __init__(self, master, usuario):
        """
        Inicializa la ventana de reportes.
        
        Args:
            master (tk.Tk): Ventana principal.
            usuario (str): Nombre del usuario.
        """
        self.master = master
        self.master.title("Mis Reportes")
        self.master.geometry("400x300")
        self.usuario = usuario

        # Título con el nombre del usuario
        tk.Label(master, text=f"Reportes de {self.usuario}", font=("Arial", 12, "bold")).pack(pady=10)

        # Carga los reportes y muestra
        reportes = self.cargar_reportes()
        if not reportes:
            tk.Label(master, text="No has enviado reportes.").pack(pady=10)
        else:
            for r in reportes:
                info = f"- Categoría: {r['categoria']}\n  Estado: {r['estado']}\n  Descripción: {r['contenido']}\n"
                tk.Label(master, text=info, anchor="w", justify="left", wraplength=360).pack(padx=10, pady=4)

        # Botón para cerrar la ventana
        tk.Button(master, text="Cerrar", command=self.master.destroy).pack(pady=10)

    def cargar_reportes(self):
        """
        Carga los reportes del archivo JSON para el usuario actual.

        Returns:
            list: Lista de reportes del usuario.
        """
        if not os.path.exists("reportes.json"):
            return []  # Si no existe, retorna lista vacía

        with open("reportes.json", "r") as f:
            try:
                todos = json.load(f)
                return [r for r in todos if r["usuario"] == self.usuario]  # Filtra por usuario
            except json.JSONDecodeError:
                return []  # Si error de lectura, retorna lista vacía
