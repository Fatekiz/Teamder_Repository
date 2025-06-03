import tkinter as tk
from tkinter import messagebox
import json
import os

class ReportesWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Reportar un Problema")
        self.master.geometry("400x350")
        self.usuario = usuario

        tk.Label(master, text="Selecciona la categoría del problema:", font=("Arial", 12)).pack(pady=5)
        self.categorias = ["Bug", "Ajustes de Perfil", "Acceder al Foro", "Salas de Juego", "Eventos"]
        self.categoria_seleccionada = tk.StringVar()
        self.categoria_seleccionada.set(self.categorias[0])  # valor por defecto
        tk.OptionMenu(master, self.categoria_seleccionada, *self.categorias).pack(pady=5)

        tk.Label(master, text="Describe el problema:", font=("Arial", 12)).pack(pady=5)
        self.texto = tk.Text(master, height=8, width=40)
        self.texto.pack(pady=5)

        tk.Button(master, text="Enviar Reporte", command=self.enviar_reporte).pack(pady=10)

    def enviar_reporte(self):
        contenido = self.texto.get("1.0", tk.END).strip()
        categoria = self.categoria_seleccionada.get().strip()

        if not contenido:
            messagebox.showwarning("Aviso", "El reporte no puede estar vacío.")
            return

        reporte = {
            "usuario": self.usuario,
            "categoria": categoria,
            "contenido": contenido,
            "estado": "pendiente"
        }

        if not os.path.exists("reportes.json"):
            with open("reportes.json", "w") as f:
                json.dump([], f)

        with open("reportes.json", "r") as f:
            try:
                reportes = json.load(f)
                if not isinstance(reportes, list):
                    reportes = []
            except json.JSONDecodeError:
                reportes = []

        reportes.append(reporte)

        with open("reportes.json", "w") as f:
            json.dump(reportes, f, indent=4)

        messagebox.showinfo("Enviado", "Reporte enviado correctamente.")
        self.master.destroy()
        self.mostrar_estado_reportes()

    def mostrar_estado_reportes(self):
        estado_window = tk.Tk()
        estado_window.title("Estado de tus reportes")
        estado_window.geometry("400x300")

        tk.Label(estado_window, text=f"Reportes de {self.usuario}", font=("Arial", 12, "bold")).pack(pady=10)

        try:
            with open("reportes.json", "r") as f:
                reportes = json.load(f)
        except:
            reportes = []

        reportes_usuario = [r for r in reportes if r["usuario"] == self.usuario]

        if not reportes_usuario:
            tk.Label(estado_window, text="No has enviado reportes todavía.").pack(pady=10)
        else:
            for r in reportes_usuario:
                texto = f"- Categoría: {r['categoria']} | Estado: {r['estado']}"
                tk.Label(estado_window, text=texto, wraplength=350, justify="left").pack(anchor="w", padx=20)

        tk.Button(estado_window, text="Cerrar", command=estado_window.destroy).pack(pady=10)
