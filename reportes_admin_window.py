import tkinter as tk
from tkinter import messagebox
import json
import os

class ReportesAdminWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestión de Reportes")
        self.master.geometry("600x400")

        tk.Label(master, text="Lista de Reportes", font=("Arial", 14)).pack(pady=10)

        self.lista = tk.Listbox(master, width=80)
        self.lista.pack(pady=10)

        self.boton_resuelto = tk.Button(master, text="Marcar como resuelto", command=self.marcar_resuelto)
        self.boton_resuelto.pack(pady=5)

        self.boton_eliminar = tk.Button(master, text="Eliminar reporte seleccionado", command=self.eliminar_reporte)
        self.boton_eliminar.pack(pady=5)

        self.cargar_reportes()

    def cargar_reportes(self):
        self.lista.delete(0, tk.END)
        if not os.path.exists("reportes.json"):
            return

        with open("reportes.json", "r") as f:
            try:
                self.reportes = json.load(f)
            except json.JSONDecodeError:
                self.reportes = []

        for idx, reporte in enumerate(self.reportes):
            usuario = reporte.get("usuario", "desconocido")
            categoria = reporte.get("categoria", "No especificada")
            contenido = reporte.get("contenido", "")
            estado = reporte.get("estado", "pendiente")

            texto = f"{usuario} (usuario) | Categoría: {categoria} | Estado: {estado}\nDescripción: {contenido}"
            self.lista.insert(tk.END, texto)
            self.lista.insert(tk.END, "—" * 100)  # Separador visual

    def guardar_reportes(self):
        with open("reportes.json", "w") as f:
            json.dump(self.reportes, f, indent=4)

    def marcar_resuelto(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un reporte.")
            return

        # Cada reporte ocupa 2 líneas: el contenido y el separador
        indice_real = seleccion[0] // 2
        if indice_real < len(self.reportes):
            self.reportes[indice_real]["estado"] = "resuelto"
            self.guardar_reportes()
            self.cargar_reportes()

    def eliminar_reporte(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un reporte.")
            return

        indice_real = seleccion[0] // 2
        if indice_real < len(self.reportes):
            del self.reportes[indice_real]
            self.guardar_reportes()
            self.cargar_reportes()
