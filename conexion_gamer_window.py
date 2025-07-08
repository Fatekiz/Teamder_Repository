import tkinter as tk
from tkinter import messagebox
import json
import os
from chat_window import ChatWindow  # Para abrir chats

JUEGOS_DISPONIBLES = [
    "Valorant", "League of Legends", "Fortnite", "Apex Legends",
    "Minecraft", "Counter Strike 2", "Rocket League", "Overwatch 2"
]

RUTA_USUARIOS = "usuarios.json"

def abrir_conexion_gamer(master, usuario_actual):
    ventana = master
    ventana.title("Conexión Gamer")
    ventana.geometry("600x600")

    tk.Label(ventana, text="🎮 Bienvenido a Conexión Gamer", font=("Arial", 16)).pack(pady=10)
    tk.Label(ventana, text="Selecciona hasta 5 juegos favoritos para encontrar otros usuarios con gustos similares. "
                            "También puedes escribir un juego manualmente.", wraplength=550).pack(pady=5)

    juegos_favoritos = []
    juegos_personalizados = []
    if os.path.exists(RUTA_USUARIOS):
        try:
            with open(RUTA_USUARIOS, "r") as f:
                usuarios = json.load(f)
                if usuario_actual in usuarios:
                    juegos_favoritos = usuarios[usuario_actual].get("juegos_favoritos", [])
                    juegos_personalizados = usuarios[usuario_actual].get("juegos_personalizados", [])
        except json.JSONDecodeError:
            pass

    frame_juegos = tk.Frame(ventana)
    frame_juegos.pack(pady=10)

    variables = []
    for juego in JUEGOS_DISPONIBLES:
        var = tk.BooleanVar()
        if juego in juegos_favoritos:
            var.set(True)
        cb = tk.Checkbutton(frame_juegos, text=juego, variable=var)
        cb.pack(anchor="w")
        variables.append((juego, var))

    frame_personalizado = tk.Frame(ventana)
    frame_personalizado.pack(pady=10)
    tk.Label(frame_personalizado, text="¿Otro juego? Escríbelo aquí:").pack()
    entry_juego_extra = tk.Entry(frame_personalizado, width=40)
    entry_juego_extra.pack()

    # Si hay juego personalizado previo, mostrarlo en el entry (solo el primero si hay varios)
    if juegos_personalizados:
        entry_juego_extra.insert(0, juegos_personalizados[0])

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

        # Validar duplicados y máximo de juegos
        total_juegos = len(seleccionados) + (1 if juego_extra else 0)
        if total_juegos == 0:
            messagebox.showwarning("Atención", "Debes seleccionar al menos un juego o escribir uno.")
            return
        if total_juegos > 5:
            messagebox.showwarning("Límite excedido", "Solo puedes elegir hasta 5 juegos en total.")
            return

        # Guardar en JSON separado
        if usuario_actual in usuarios:
            usuarios[usuario_actual]["juegos_favoritos"] = seleccionados
            usuarios[usuario_actual]["juegos_personalizados"] = [juego_extra] if juego_extra else []
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

        if usuario_actual not in usuarios:
            messagebox.showwarning("Sin preferencias", "Primero debes confirmar tus preferencias.")
            return

        mis_juegos = usuarios[usuario_actual].get("juegos_favoritos", []) + usuarios[usuario_actual].get("juegos_personalizados", [])
        if not mis_juegos:
            messagebox.showwarning("Sin preferencias", "Primero debes confirmar tus preferencias.")
            return

        nonlocal frame_resultados
        frame_resultados.destroy()
        mostrar_resultados(usuarios, usuario_actual, mis_juegos)

    def eliminar_preferencias():
        if not os.path.exists(RUTA_USUARIOS):
            messagebox.showerror("Error", "No se encontró usuarios.json")
            return

        with open(RUTA_USUARIOS, "r") as f:
            usuarios = json.load(f)

        if usuario_actual in usuarios and ("juegos_favoritos" in usuarios[usuario_actual] or "juegos_personalizados" in usuarios[usuario_actual]):
            confirmar = messagebox.askyesno("Confirmar eliminación", "¿Seguro quieres eliminar tus preferencias de juegos?")
            if confirmar:
                usuarios[usuario_actual].pop("juegos_favoritos", None)
                usuarios[usuario_actual].pop("juegos_personalizados", None)
                with open(RUTA_USUARIOS, "w") as f:
                    json.dump(usuarios, f, indent=4)
                messagebox.showinfo("Eliminado", "Tus preferencias fueron eliminadas ✅")

                # Limpiar UI
                entry_juego_extra.delete(0, tk.END)
                for _, var in variables:
                    var.set(False)
                frame_resultados.destroy()
        else:
            messagebox.showinfo("Sin preferencias", "No hay preferencias que eliminar.")

    def mostrar_resultados(usuarios, usuario_actual, mis_juegos):
        nonlocal frame_resultados
        frame_resultados = tk.Frame(ventana)
        frame_resultados.pack(pady=10)

        coincidencias = []
        for usuario, data in usuarios.items():
            if usuario == usuario_actual or "juegos_favoritos" not in data:
                continue
            juegos_otros = data.get("juegos_favoritos", []) + data.get("juegos_personalizados", [])
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

    tk.Button(frame_botones, text=" Confirmar preferencias", command=confirmar_preferencias).pack(side="left", padx=10)
    tk.Button(frame_botones, text=" Buscar coincidencias", command=buscar_coincidencias).pack(side="left", padx=10)
    tk.Button(frame_botones, text=" Borrar preferencias", command=eliminar_preferencias).pack(side="left", padx=10)
