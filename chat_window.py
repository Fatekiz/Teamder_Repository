# Importamos las bibliotecas necesarias
import tkinter as tk
import json
import os
from datetime import datetime

class ChatWindow:
    """
    Clase que representa una ventana de chat entre dos usuarios.
    Permite enviar y visualizar mensajes almacenados en un archivo JSON.
    """

    def __init__(self, usuario_actual, otro_usuario, mensaje_inicial=None):
        """
        Inicializa la ventana del chat entre el usuario actual y otro usuario.

        Parámetros:
        - usuario_actual: el nombre del usuario que inició sesión.
        - otro_usuario: el nombre del otro usuario con el que se chatea.
        - mensaje_inicial: (opcional) mensaje inicial que se desea guardar automáticamente.
        """
        self.usuario_actual = usuario_actual
        self.otro_usuario = otro_usuario
        self.archivo = "mensajes_chat.json"

        # Si el archivo de mensajes no existe, lo creamos vacío
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump([], f)

        # Creamos la interfaz de la ventana de chat
        self.root = tk.Toplevel()
        self.root.title(f"Chat con {otro_usuario}")
        self.root.geometry("400x500")

        # Área de texto donde se muestra la conversación
        self.chat_box = tk.Text(self.root, state="disabled", wrap="word")
        self.chat_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Entrada de texto para escribir mensajes
        self.entry_msg = tk.Entry(self.root)
        self.entry_msg.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        # Botón para enviar el mensaje
        self.btn_send = tk.Button(self.root, text="Enviar", command=self.enviar_mensaje)
        self.btn_send.pack(side="right", padx=5, pady=5)

        # Si se proporciona un mensaje inicial, lo guardamos automáticamente
        if mensaje_inicial:
            self.guardar_mensaje(mensaje_inicial)

        # Mostramos la conversación existente en la ventana
        self.mostrar_conversacion()

    def guardar_mensaje(self, contenido):
        """
        Guarda un nuevo mensaje en el archivo JSON.

        Parámetro:
        - contenido: texto del mensaje que se desea guardar.
        """
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
        """
        Muestra todos los mensajes entre el usuario actual y el otro usuario.
        """
        with open(self.archivo, "r") as f:
            mensajes = json.load(f)

        # Filtramos solo los mensajes entre estos dos usuarios
        conversacion = [
            m for m in mensajes if
            (m["remitente"] == self.usuario_actual and m["destinatario"] == self.otro_usuario) or
            (m["remitente"] == self.otro_usuario and m["destinatario"] == self.usuario_actual)
        ]

        # Mostramos los mensajes en la caja de texto
        self.chat_box.config(state="normal")
        self.chat_box.delete(1.0, tk.END)
        for m in conversacion:
            self.chat_box.insert(
                tk.END,
                f"{m['remitente']} ({m['fecha']}):\n{m['mensaje']}\n\n"
            )
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)  # Hace scroll al final

    def enviar_mensaje(self):
        """
        Obtiene el mensaje del Entry, lo guarda y actualiza la conversación.
        """
        texto = self.entry_msg.get().strip()
        if texto:
            self.guardar_mensaje(texto)
            self.entry_msg.delete(0, tk.END)
            self.mostrar_conversacion()