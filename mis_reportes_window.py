import tkinter as tk
import json
import os

class MisReportesWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Mis Reportes")
        self.master.geometry("400x300")
        self.usuario = usuario

        tk.Label(master, text=f"Reportes de {self.usuario}", font=("Arial", 12, "bold")).pack(pady=10)

        reportes = self.cargar_reportes()

        if not reportes:
            tk.Label(master, text="No has enviado reportes.").pack(pady=10)
        else:
            for r in reportes:
                info = f"- Categoría: {r['categoria']}\n  Estado: {r['estado']}\n  Descripción: {r['contenido']}\n"
                tk.Label(master, text=info, anchor="w", justify="left", wraplength=360).pack(padx=10, pady=4)

        tk.Button(master, text="Cerrar", command=self.master.destroy).pack(pady=10)

    def cargar_reportes(self):
        if not os.path.exists("reportes.json"):
            return []

        with open("reportes.json", "r") as f:
            try:
                todos = json.load(f)
                return [r for r in todos if r["usuario"] == self.usuario]
            except json.JSONDecodeError:
                return []
