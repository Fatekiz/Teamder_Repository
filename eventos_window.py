# eventos_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

class EventosWindow:
    def __init__(self, master, usuario,is_admin):
        self.master = master
        self.usuario = usuario
        self.is_admin = is_admin
        self.master.title("Eventos")
        self.master.geometry("700x500")
        self.archivo = "eventos.json"
        self.eventos = []
        self.cargar_eventos()
        self.crear_widgets()

    def cargar_eventos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.eventos = json.load(f)
        else:
            self.eventos = []
            self.guardar_eventos()

    def guardar_eventos(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.eventos, f, indent=4, ensure_ascii=False)

    def crear_widgets(self):
        frame_superior = tk.Frame(self.master)
        frame_superior.pack(pady=10)

        tk.Button(frame_superior, text="Crear Evento", command=self.crear_evento).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_superior, text="Actualizar", command=self.actualizar_lista).pack(side=tk.LEFT, padx=10)

        self.lista_eventos = ttk.Treeview(self.master, columns=("titulo", "fecha", "hora", "creador"), show="headings")
        self.lista_eventos.heading("titulo", text="Título")
        self.lista_eventos.heading("fecha", text="Fecha")
        self.lista_eventos.heading("hora", text="Hora")
        self.lista_eventos.heading("creador", text="Creador")
        self.lista_eventos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lista_eventos.bind("<<TreeviewSelect>>", self.ver_evento)

        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_eventos.delete(*self.lista_eventos.get_children())
        for evento in self.eventos:
            self.lista_eventos.insert("", tk.END, iid=str(evento["id"]),
                                      values=(evento["titulo"], evento["fecha"], evento["hora"], evento["creador"]))

    def crear_evento(self):
        ventana_nuevo = tk.Toplevel(self.master)
        ventana_nuevo.title("Crear nuevo evento")
        ventana_nuevo.geometry("400x400")
        tk.Label(ventana_nuevo, text="Título:").pack(pady=5)
        entry_titulo = tk.Entry(ventana_nuevo)
        entry_titulo.pack(pady=5)

        tk.Label(ventana_nuevo, text="Descripción:").pack(pady=5)
        text_descripcion = tk.Text(ventana_nuevo, height=5)
        text_descripcion.pack(pady=5)

        tk.Label(ventana_nuevo, text="Fecha (DD-MM-YYYY):").pack(pady=5)
        entry_fecha = tk.Entry(ventana_nuevo)
        entry_fecha.pack(pady=5)

        tk.Label(ventana_nuevo, text="Hora (HH:MM):").pack(pady=5)
        entry_hora = tk.Entry(ventana_nuevo)
        entry_hora.pack(pady=5)

        def guardar():
            titulo = entry_titulo.get().strip()
            descripcion = text_descripcion.get("1.0", tk.END).strip()
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip()

            if not titulo or not descripcion or not fecha or not hora:
                messagebox.showerror("Error", "Completa todos los campos.")
                return

            try:
                datetime.datetime.strptime(fecha, "%d-%m-%Y")
                datetime.datetime.strptime(hora, "%H:%M")
            except ValueError:
                messagebox.showerror("Error", "Fecha u hora inválida.")
                return

            nuevo_id = max((e["id"] for e in self.eventos), default=0) + 1
            nuevo_evento = {
                "id": nuevo_id,
                "titulo": titulo,
                "descripcion": descripcion,
                "fecha": fecha,
                "hora": hora,
                "creador": self.usuario,
                "inscritos": []
            }

            self.eventos.append(nuevo_evento)
            self.guardar_eventos()
            self.actualizar_lista()
            ventana_nuevo.destroy()
            messagebox.showinfo("Éxito", "Evento creado correctamente.")

        tk.Button(ventana_nuevo, text="Guardar evento", command=guardar).pack(pady=10)


    def ver_evento(self, evento):
        seleccion = self.lista_eventos.selection()
        if not seleccion:
            return

        evento_id = int(seleccion[0])
        evento = next((e for e in self.eventos if e["id"] == evento_id), None)
        if not evento:
            return

        ventana_detalle = tk.Toplevel(self.master)
        ventana_detalle.title("Detalles del Evento")
        ventana_detalle.geometry("400x400")

        inscritos = evento.get("inscritos", [])

        # Mostrar info
        tk.Label(ventana_detalle, text=f"Título: {evento['titulo']}", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(ventana_detalle, text=f"Fecha: {evento['fecha']}").pack()
        tk.Label(ventana_detalle, text=f"Hora: {evento['hora']}").pack()
        tk.Label(ventana_detalle, text=f"Descripción:\n{evento['descripcion']}").pack(pady=10)
        tk.Label(ventana_detalle, text=f"Inscritos: {len(inscritos)}").pack()

        # Lista de inscritos (opcional, mostrar nombres)
        if inscritos:
            tk.Label(ventana_detalle, text="Usuarios inscritos:").pack()
            for user in inscritos:
                tk.Label(ventana_detalle, text=f"- {user}").pack()

        # Inscripción
        if self.usuario not in inscritos:
            def inscribirse():
                evento["inscritos"].append(self.usuario)
                self.guardar_eventos()
                ventana_detalle.destroy()
                messagebox.showinfo("Éxito", "Te has inscrito al evento.")
                self.actualizar_lista()

            tk.Button(ventana_detalle, text="Inscribirme", command=inscribirse).pack(pady=10)
        else:
            def desinscribirse():
                if messagebox.askyesno("Confirmar", "¿Quieres desinscribirte del evento?"):
                    evento["inscritos"].remove(self.usuario)
                    self.guardar_eventos()
                    ventana_detalle.destroy()
                    messagebox.showinfo("Listo", "Te desinscribiste del evento.")
                    self.actualizar_lista()

            tk.Label(ventana_detalle, text="Ya estás inscrito en este evento.").pack(pady=5)
            tk.Button(ventana_detalle, text="Desinscribirme", command=desinscribirse).pack(pady=5)

        # Si el usuario es el creador o admin, puede editar/eliminar
        if self.is_admin or self.usuario == evento["creador"]:
            def editar_evento():
                ventana_detalle.destroy()
                self.abrir_edicion_evento(evento)

            def eliminar_evento():
                if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este evento?"):
                    self.eventos = [e for e in self.eventos if e["id"] != evento["id"]]
                    self.guardar_eventos()
                    ventana_detalle.destroy()
                    self.actualizar_lista()
                    messagebox.showinfo("Éxito", "Evento eliminado correctamente.")

            tk.Button(ventana_detalle, text="Editar Evento", command=editar_evento).pack(pady=5)
            tk.Button(ventana_detalle, text="Eliminar Evento", command=eliminar_evento).pack(pady=5)

    def abrir_edicion_evento(self, evento):
        ventana_editar = tk.Toplevel(self.master)
        ventana_editar.title("Editar evento")
        ventana_editar.geometry("400x400")

        # Campos precargados
        entry_titulo = tk.Entry(ventana_editar)
        entry_titulo.insert(0, evento["titulo"])
        entry_titulo.pack(pady=5)

        text_descripcion = tk.Text(ventana_editar, height=5)
        text_descripcion.insert(tk.END, evento["descripcion"])
        text_descripcion.pack(pady=5)

        entry_fecha = tk.Entry(ventana_editar)
        entry_fecha.insert(0, evento["fecha"])
        entry_fecha.pack(pady=5)

        entry_hora = tk.Entry(ventana_editar)
        entry_hora.insert(0, evento["hora"])
        entry_hora.pack(pady=5)

        def guardar_cambios():
            titulo = entry_titulo.get().strip()
            descripcion = text_descripcion.get("1.0", tk.END).strip()
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip()

            if not titulo or not descripcion or not fecha or not hora:
                messagebox.showerror("Error", "Completa todos los campos.")
                return

            try:
                datetime.datetime.strptime(fecha, "%d-%m-%Y")
                datetime.datetime.strptime(hora, "%H:%M")
            except ValueError:
                messagebox.showerror("Error", "Fecha u hora inválida.")
                return

            evento["titulo"] = titulo
            evento["descripcion"] = descripcion
            evento["fecha"] = fecha
            evento["hora"] = hora

            self.guardar_eventos()
            self.actualizar_lista()
            ventana_editar.destroy()
            messagebox.showinfo("Éxito", "Evento actualizado correctamente.")

        tk.Button(ventana_editar, text="Guardar cambios", command=guardar_cambios).pack(pady=10)
