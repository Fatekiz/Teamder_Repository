import tkinter as tk
import json
import os
from datetime import datetime

class ChatWindow:
    def __init__(self, usuario_actual, otro_usuario, mensaje_inicial=None):
        self.usuario_actual = usuario_actual
        self.otro_usuario = otro_usuario
        self.archivo = "mensajes_chat.json"

        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump([], f)

        self.root = tk.Toplevel()
        self.root.title(f"Chat con {otro_usuario}")
        self.root.geometry("400x500")

        self.chat_box = tk.Text(self.root, state="disabled", wrap="word")
        self.chat_box.pack(expand=True, fill="both", padx=10, pady=10)

        self.entry_msg = tk.Entry(self.root)
        self.entry_msg.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        self.btn_send = tk.Button(self.root, text="Enviar", command=self.enviar_mensaje)
        self.btn_send.pack(side="right", padx=5, pady=5)

        if mensaje_inicial:
            self.guardar_mensaje(mensaje_inicial)

        self.mostrar_conversacion()

    def guardar_mensaje(self, contenido):
        with open(self.archivo, "r") as f:
            mensajes = json.load(f)

        mensajes.append({
            "remitente": self.usuario_actual,
            "destinatario": self.otro_usuario,
            "mensaje": contenido,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        with open(self.archivo, "w") as f:
            json.dump(mensajes, f, indent=4)

    def mostrar_conversacion(self):
        with open(self.archivo, "r") as f:
            mensajes = json.load(f)

        conversacion = [
            m for m in mensajes if
            (m["remitente"] == self.usuario_actual and m["destinatario"] == self.otro_usuario) or
            (m["remitente"] == self.otro_usuario and m["destinatario"] == self.usuario_actual)
        ]

        self.chat_box.config(state="normal")
        self.chat_box.delete(1.0, tk.END)
        for m in conversacion:
            self.chat_box.insert(tk.END, f"{m['remitente']} ({m['fecha']}):\n{m['mensaje']}\n\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    def enviar_mensaje(self):
        texto = self.entry_msg.get().strip()
        if texto:
            self.guardar_mensaje(texto)
            self.entry_msg.delete(0, tk.END)
            self.mostrar_conversacion()