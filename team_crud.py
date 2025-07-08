import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# -----------------------------------------------------------------------------
# team_crud.py – CRUD de Equipos para Teamder
# -----------------------------------------------------------------------------
# Este módulo implementa una interfaz Tkinter que permite a los usuarios crear,
# leer, actualizar y eliminar equipos dentro de la aplicación Teamder.
# Cada equipo está compuesto por un id numérico, un nombre, una descripción,
# el nombre del usuario creador y la lista de miembros.
# Se guarda todo en un archivo local JSON (equipos.json) para simplificar.
# El estilo y patrón de código imitan al resto del proyecto para encajar con
# los otros *_window.py.
# -----------------------------------------------------------------------------

ARCHIVO_EQUIPOS = "equipos.json"

# -----------------------------------------------------------------------------
# Funciones de persistencia
# -----------------------------------------------------------------------------

def _cargar_equipos():
    """Devuelve la lista de equipos almacenados en equipos.json."""
    if not os.path.exists(ARCHIVO_EQUIPOS):
        with open(ARCHIVO_EQUIPOS, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    with open(ARCHIVO_EQUIPOS, "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar_equipos(equipos):
    """Sobrescribe equipos.json con la lista dada."""
    with open(ARCHIVO_EQUIPOS, "w", encoding="utf-8") as f:
        json.dump(equipos, f, ensure_ascii=False, indent=4)

# -----------------------------------------------------------------------------
# Ventana principal del CRUD
# -----------------------------------------------------------------------------

def abrir_crud_equipos(master: tk.Tk | tk.Toplevel, usuario_actual: str) -> None:
    """Abre la ventana de gestión de equipos sobre el *master* indicado."""

    is_admin = str(usuario_actual).lower() == "admin" or getattr(usuario_actual, "is_admin", False)

    # ---------------------------------------------------------------------
    # Helpers internos (definidos dentro para acceder a *equipos* y widgets)
    # ---------------------------------------------------------------------
    def _refrescar_listbox():
        listbox.delete(0, tk.END)
        equipos[:] = _cargar_equipos()  # recargar desde disco
        for eq in equipos:
            miembros = len(eq["miembros"])
            listbox.insert(tk.END, f"{eq['nombre']}  ( {miembros} miembro{'s' if miembros!=1 else ''} )")

    def _crear_equipo():
        nombre = simpledialog.askstring("Nuevo Equipo", "Nombre del equipo:", parent=ventana)
        if not nombre or not nombre.strip():
            messagebox.showerror("Error", "El nombre del equipo no puede estar vacío.")
            return
        nombre = nombre.strip()
        # Comprobar unicidad (case‑insensitive)
        if any(eq["nombre"].lower() == nombre.lower() for eq in equipos):
            messagebox.showerror("Error", "Ya existe un equipo con ese nombre.")
            return
        descripcion = simpledialog.askstring("Nuevo Equipo", "Descripción del equipo:", parent=ventana) or ""
        nuevo = {
            "id": max([eq["id"] for eq in equipos] + [0]) + 1,
            "nombre": nombre,
            "descripcion": descripcion,
            "creador": usuario_actual,
            "miembros": [usuario_actual],
        }
        equipos.append(nuevo)
        _guardar_equipos(equipos)
        _refrescar_listbox()

    def _seleccionar_equipo() -> dict | None:
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Sin selección", "Selecciona un equipo de la lista.")
            return None
        return equipos[sel[0]]

    def _editar_equipo():
        equipo = _seleccionar_equipo()
        if not equipo:
            return
        if usuario_actual != equipo["creador"]:
            messagebox.showerror("Permiso denegado", "Solo el creador puede editar el equipo.")
            return
        nuevo_nombre = simpledialog.askstring("Editar Equipo", "Nuevo nombre:", initialvalue=equipo["nombre"], parent=ventana)
        if not nuevo_nombre:
            return
        nueva_desc = simpledialog.askstring("Editar Equipo", "Nueva descripción:", initialvalue=equipo["descripcion"], parent=ventana) or equipo["descripcion"]
        equipo["nombre"] = nuevo_nombre
        equipo["descripcion"] = nueva_desc
        _guardar_equipos(equipos)
        _refrescar_listbox()

    def _eliminar_equipo():
        equipo = _seleccionar_equipo()
        if not equipo:
            return
        # Permitir al admin eliminar cualquier equipo
        if not is_admin and usuario_actual != equipo["creador"]:
            messagebox.showerror("Permiso denegado", "Solo el creador o un administrador pueden eliminar el equipo.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar el equipo '{equipo['nombre']}' definitivamente?"):
            equipos.remove(equipo)
            _guardar_equipos(equipos)
            _refrescar_listbox()

    def _unirse_equipo():
        equipo = _seleccionar_equipo()
        if not equipo:
            return
        if usuario_actual in equipo["miembros"]:
            messagebox.showinfo("Info", "Ya formas parte de este equipo.")
            return
        equipo["miembros"].append(usuario_actual)
        _guardar_equipos(equipos)
        _refrescar_listbox()

    def _salir_equipo():
        equipo = _seleccionar_equipo()
        if not equipo:
            return
        if usuario_actual not in equipo["miembros"]:
            messagebox.showinfo("Info", "No perteneces a este equipo.")
            return
        if usuario_actual == equipo["creador"]:
            messagebox.showerror("Error", "El creador no puede salir: debe eliminar el equipo o transferir la propiedad.")
            return
        equipo["miembros"].remove(usuario_actual)
        _guardar_equipos(equipos)
        _refrescar_listbox()

    # ---------------------------------------------------------------------
    # Ventana y widgets
    # ---------------------------------------------------------------------
    ventana = master
    ventana.title("Gestión de Equipos")
    ventana.geometry("450x550")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Gestión de Equipos", font=("Arial", 16, "bold")).pack(pady=10)

    # Listbox para mostrar equipos
    listbox = tk.Listbox(ventana, width=55, height=18)
    listbox.pack(pady=5)

    # Cargar datos
    equipos = _cargar_equipos()
    _refrescar_listbox()

    # Frame de botones principales
    frame_top = tk.Frame(ventana)
    frame_top.pack(pady=8)

    tk.Button(frame_top, text="Crear", width=10, command=_crear_equipo).grid(row=0, column=0, padx=3, pady=2)
    tk.Button(frame_top, text="Editar", width=10, command=_editar_equipo).grid(row=0, column=1, padx=3, pady=2)
    tk.Button(frame_top, text="Eliminar", width=10, command=_eliminar_equipo).grid(row=0, column=2, padx=3, pady=2)

    frame_mid = tk.Frame(ventana)
    frame_mid.pack(pady=4)

    tk.Button(frame_mid, text="Unirme", width=10, command=_unirse_equipo).grid(row=0, column=0, padx=3, pady=2)
    tk.Button(frame_mid, text="Salir", width=10, command=_salir_equipo).grid(row=0, column=1, padx=3, pady=2)

    tk.Button(ventana, text="Cerrar", width=10, command=ventana.destroy).pack(pady=10)
