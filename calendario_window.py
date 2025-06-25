import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class CalendarioWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Mi Calendario Personal")
        self.master.geometry("600x500")
        self.usuario = usuario
        self.archivo = "calendario.json"
        self.recordatorios = []

        self.cargar_datos()
        self.crear_widgets()
        self.actualizar_lista()

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.recordatorios = datos.get(self.usuario, [])
        else:
            self.recordatorios = []

    def guardar_datos(self):
        datos = {}
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        datos[self.usuario] = self.recordatorios
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def crear_widgets(self):
        tk.Button(self.master, text="Agregar Recordatorio", command=self.agregar_recordatorio).pack(pady=10)

        self.lista = ttk.Treeview(self.master, columns=("fecha", "titulo"), show="headings")
        self.lista.heading("fecha", text="Fecha")
        self.lista.heading("titulo", text="Título")
        self.lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lista.bind("<<TreeviewSelect>>", self.ver_recordatorio)

    def actualizar_lista(self):
        self.lista.delete(*self.lista.get_children())
        for i, rec in enumerate(self.recordatorios):
            self.lista.insert("", "end", iid=str(i), values=(rec["fecha"], rec["titulo"]))

    def agregar_recordatorio(self):
        self.ventana_edicion(None)

    def ver_recordatorio(self, event):
        seleccion = self.lista.selection()
        if not seleccion:
            return
        index = int(seleccion[0])
        self.ventana_edicion(index)

    def ventana_edicion(self, index):
        ventana = tk.Toplevel(self.master)
        ventana.title("Editar Recordatorio" if index is not None else "Nuevo Recordatorio")
        ventana.geometry("400x350")

        tk.Label(ventana, text="Título:").pack(pady=5)
        entry_titulo = tk.Entry(ventana)
        entry_titulo.pack(pady=5)

        tk.Label(ventana, text="Fecha (YYYY-MM-DD):").pack(pady=5)
        entry_fecha = tk.Entry(ventana)
        entry_fecha.pack(pady=5)

        tk.Label(ventana, text="Nota:").pack(pady=5)
        text_nota = tk.Text(ventana, height=8)
        text_nota.pack(pady=5)

        if index is not None:
            recordatorio = self.recordatorios[index]
            entry_titulo.insert(0, recordatorio["titulo"])
            entry_fecha.insert(0, recordatorio["fecha"])
            text_nota.insert("1.0", recordatorio["nota"])

        def guardar():
            titulo = entry_titulo.get().strip()
            fecha = entry_fecha.get().strip()
            nota = text_nota.get("1.0", tk.END).strip()

            if not titulo or not fecha or not nota:
                messagebox.showerror("Error", "Completa todos los campos.")
                return

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD.")
                return

            nuevo = {
                "titulo": titulo,
                "fecha": fecha,
                "nota": nota
            }

            if index is not None:
                self.recordatorios[index] = nuevo
            else:
                self.recordatorios.append(nuevo)

            self.guardar_datos()
            self.actualizar_lista()
            ventana.destroy()
            messagebox.showinfo("Éxito", "Recordatorio guardado.")

        def eliminar():
            if index is not None:
                if messagebox.askyesno("Confirmar", "¿Eliminar este recordatorio?"):
                    self.recordatorios.pop(index)
                    self.guardar_datos()
                    self.actualizar_lista()
                    ventana.destroy()
                    messagebox.showinfo("Eliminado", "Recordatorio eliminado.")

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

        if index is not None:
            tk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=5)
