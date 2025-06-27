import tkinter as tk
from tkinter import messagebox
import json
import os
from chat_window import ChatWindow

JUEGOS_DISPONIBLES = [
    "Valorant", "League of Legends", "Fortnite", "Apex Legends",
    "Minecraft", "Counter Strike 2", "Rocket League", "Overwatch 2"
]

RUTA_USUARIOS = "usuarios.json"

def abrir_conexion_gamer(master, usuario_actual):
    ventana = tk.Toplevel(master)
    ventana.title("Conexión Gamer")
    ventana.geometry("600x600")

    tk.Label(ventana, text="🎮 Bienvenido a Conexión Gamer", font=("Arial", 16)).pack(pady=10)
    tk.Label(ventana, text="Selecciona hasta 5 juegos favoritos para encontrar otros usuarios con gustos similares. "
                            "También puedes escribir un juego manualmente.", wraplength=550).pack(pady=5)

    frame_juegos = tk.Frame(ventana)
    frame_juegos.pack(pady=10)

    variables = []
    for juego in JUEGOS_DISPONIBLES:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(frame_juegos, text=juego, variable=var)
        cb.pack(anchor="w")
        variables.append((juego, var))

    frame_personalizado = tk.Frame(ventana)
    frame_personalizado.pack(pady=10)
    tk.Label(frame_personalizado, text="¿Otro juego? Escríbelo aquí:").pack()
    entry_juego_extra = tk.Entry(frame_personalizado, width=40)
    entry_juego_extra.pack()

    frame_resultados = tk.Frame(ventana)
    frame_resultados.pack(pady=10)

    def confirmar_preferencias():
        if not os.path.exists(RUTA_USUARIOS):
            messagebox.showerror("Error", "No se encontró usuarios.json")
            return

        try:
            with open(RUTA_USUARIOS, "r") as f:
                usuarios = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer usuarios.json")
            return

        seleccionados = [j for j, var in variables if var.get()]
        juego_extra = entry_juego_extra.get().strip().title()
        if juego_extra:
            seleccionados.append(juego_extra)

        seleccionados = list(set(seleccionados))

        if len(seleccionados) == 0:
            messagebox.showwarning("Atención", "Debes seleccionar al menos un juego.")
            return
        if len(seleccionados) > 5:
            messagebox.showwarning("Límite excedido", "Solo puedes elegir hasta 5 juegos.")
            return

        if usuario_actual in usuarios:
            usuarios[usuario_actual]["juegos_favoritos"] = seleccionados
        else:
            messagebox.showerror("Error", "Usuario no encontrado en la base de datos.")
            return

        with open(RUTA_USUARIOS, "w") as f:
            json.dump(usuarios, f, indent=4)

        messagebox.showinfo("Guardado", "Preferencias guardadas correctamente ✅")

    def buscar_coincidencias():
        if not os.path.exists(RUTA_USUARIOS):
            messagebox.showerror("Error", "No se encontró usuarios.json")
            return

        with open(RUTA_USUARIOS, "r") as f:
            usuarios = json.load(f)

        if usuario_actual not in usuarios or "juegos_favoritos" not in usuarios[usuario_actual]:
            messagebox.showwarning("Sin preferencias", "Primero debes confirmar tus preferencias.")
            return

        seleccionados = usuarios[usuario_actual]["juegos_favoritos"]

        nonlocal frame_resultados
        frame_resultados.destroy()
        mostrar_resultados(usuarios, usuario_actual, seleccionados)

    def mostrar_resultados(usuarios, usuario_actual, mis_juegos):
        nonlocal frame_resultados
        frame_resultados = tk.Frame(ventana)
        frame_resultados.pack(pady=10)

        coincidencias = []
        for usuario, data in usuarios.items():
            if usuario == usuario_actual or "juegos_favoritos" not in data:
                continue
            juegos_otros = data["juegos_favoritos"]
            en_comun = set(mis_juegos) & set(juegos_otros)
            if en_comun:
                coincidencias.append((usuario, len(en_comun), list(en_comun)))

        if not coincidencias:
            tk.Label(frame_resultados, text="No se encontraron coincidencias 🥲").pack()
            return

        coincidencias.sort(key=lambda x: x[1], reverse=True)

        tk.Label(frame_resultados, text="Usuarios con juegos en común:", font=("Arial", 12, "bold")).pack(pady=5)

        for usuario, cantidad, juegos in coincidencias:
            texto = f"{usuario} - {cantidad} en común: {', '.join(juegos)}"
            frame = tk.Frame(frame_resultados)
            frame.pack(fill="x", padx=10, pady=2)
            tk.Label(frame, text=texto).pack(side="left")
            tk.Button(frame, text="Chatear", command=lambda u=usuario: ChatWindow(usuario_actual, u)).pack(side="right")

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="✅ Confirmar preferencias", command=confirmar_preferencias).pack(side="left", padx=10)
    tk.Button(frame_botones, text="🔍 Buscar coincidencias", command=buscar_coincidencias).pack(side="left", padx=10)
