# Importamos los módulos necesarios para crear la interfaz gráfica, mostrar mensajes emergentes,
# trabajar con archivos JSON y verificar la existencia de archivos.
import tkinter as tk
from tkinter import messagebox
import json
import os
from chat_window import ChatWindow  # Importamos la ventana de chat individual

def abrir_crud_chats(master, usuario_actual):
    """
    Crea una ventana que muestra los chats activos del usuario y permite abrir o eliminar conversaciones.

    Parámetros:
    - master: ventana padre desde la que se llama a esta función.
    - usuario_actual: nombre del usuario que inició sesión.
    """
    ventana = tk.Toplevel(master)
    ventana.title("Chats activos")
    ventana.geometry("400x500")

    archivo = "mensajes_chat.json"

    # Si no existe el archivo de mensajes, lo creamos vacío
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            json.dump([], f)

    # Cargamos todos los mensajes desde el archivo JSON
    with open(archivo, "r") as f:
        mensajes = json.load(f)

    # Diccionario para almacenar el último mensaje de cada chat del usuario
    chats = {}
    for m in mensajes:
        u1, u2 = m["remitente"], m["destinatario"]

        # Verificamos si el mensaje pertenece al usuario actual
        if usuario_actual in (u1, u2):
            otro = u2 if u1 == usuario_actual else u1
            key = tuple(sorted([usuario_actual, otro]))

            # Guardamos solo el mensaje más reciente para cada chat
            if key not in chats or m["fecha"] > chats[key]["fecha"]:
                chats[key] = {
                    "usuario": otro,
                    "mensaje": m["mensaje"],
                    "fecha": m["fecha"]
                }

    # Creamos una lista donde se mostrarán los chats activos
    lista = tk.Listbox(ventana, font=("Arial", 11))
    lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    chat_keys = list(chats.keys())
    for key in chat_keys:
        info = chats[key]
        # Mostramos el nombre del otro usuario y un preview del mensaje
        lista.insert(tk.END, f"{info['usuario']} → {info['mensaje'][:30]}...")

    def abrir_chat():
        """
        Abre una nueva ventana de chat con el usuario seleccionado.
        """
        seleccion = lista.curselection()
        if not seleccion:
            return
        i = seleccion[0]
        otro_usuario = chats[chat_keys[i]]["usuario"]
        ChatWindow(usuario_actual, otro_usuario)

    def eliminar_chat():
        """
        Elimina toda la conversación con el usuario seleccionado del archivo JSON.
        """
        seleccion = lista.curselection()
        if not seleccion:
            return
        i = seleccion[0]
        key = chat_keys[i]

        # Confirmamos antes de eliminar
        if not messagebox.askyesno("Confirmar", f"¿Eliminar conversación con {chats[key]['usuario']}?"):
            return

        # Filtramos los mensajes eliminando los que pertenezcan a esa conversación
        nueva_lista = [
            m for m in mensajes
            if sorted([m["remitente"], m["destinatario"]]) != list(key)
        ]

        # Sobrescribimos el archivo con la nueva lista de mensajes
        with open(archivo, "w") as f:
            json.dump(nueva_lista, f, indent=4)

        messagebox.showinfo("Eliminado", "Conversación eliminada")

        # Reiniciamos la ventana para reflejar los cambios
        ventana.destroy()
        abrir_crud_chats(master, usuario_actual)

    # Creamos los botones para abrir y eliminar chats
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=5)

    tk.Button(frame_botones, text="Abrir chat", command=abrir_chat).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="Eliminar chat", command=eliminar_chat).pack(side=tk.LEFT, padx=10)