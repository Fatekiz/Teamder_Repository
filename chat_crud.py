import tkinter as tk
from tkinter import messagebox
import json
import os
from chat_window import ChatWindow

def abrir_crud_chats(master, usuario_actual):
    ventana = tk.Toplevel(master)
    ventana.title("Chats activos")
    ventana.geometry("400x500")

    archivo = "mensajes_chat.json"
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            json.dump([], f)

    with open(archivo, "r") as f:
        mensajes = json.load(f)

    chats = {}
    for m in mensajes:
        u1, u2 = m["remitente"], m["destinatario"]
        if usuario_actual in (u1, u2):
            otro = u2 if u1 == usuario_actual else u1
            key = tuple(sorted([usuario_actual, otro]))
            if key not in chats or m["fecha"] > chats[key]["fecha"]:
                chats[key] = {
                    "usuario": otro,
                    "mensaje": m["mensaje"],
                    "fecha": m["fecha"]
                }

    lista = tk.Listbox(ventana, font=("Arial", 11))
    lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    chat_keys = list(chats.keys())
    for key in chat_keys:
        info = chats[key]
        lista.insert(tk.END, f"{info['usuario']} → {info['mensaje'][:30]}...")

    def abrir_chat():
        seleccion = lista.curselection()
        if not seleccion:
            return
        i = seleccion[0]
        otro_usuario = chats[chat_keys[i]]["usuario"]
        ChatWindow(usuario_actual, otro_usuario)

    def eliminar_chat():
        seleccion = lista.curselection()
        if not seleccion:
            return
        i = seleccion[0]
        key = chat_keys[i]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar conversación con {chats[key]['usuario']}?"):
            return
        nueva_lista = [
            m for m in mensajes
            if sorted([m["remitente"], m["destinatario"]]) != list(key)
        ]
        with open(archivo, "w") as f:
            json.dump(nueva_lista, f, indent=4)
        messagebox.showinfo("Eliminado", "Conversación eliminada")
        ventana.destroy()
        abrir_crud_chats(master, usuario_actual)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=5)

    tk.Button(frame_botones, text="Abrir chat", command=abrir_chat).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="Eliminar chat", command=eliminar_chat).pack(side=tk.LEFT, padx=10)