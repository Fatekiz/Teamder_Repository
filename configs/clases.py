import json
from configs.config import *
from tkinter import messagebox
import tkinter as tk
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("1000x900")

        # Crear un frame centrado para el formulario
        self.frame = tk.Frame(root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # Centra el frame en la ventana

        # Usuario
        tk.Label(self.frame, text="Usuario:", font=("Arial", 14)).pack(pady=10)
        self.entrada_usuario = tk.Entry(self.frame, font=("Arial", 14))
        self.entrada_usuario.pack()

        # Contraseña
        tk.Label(self.frame, text="Contraseña:", font=("Arial", 14)).pack(pady=10)
        self.entrada_contrasena = tk.Entry(self.frame, show="*", font=("Arial", 14))
        self.entrada_contrasena.pack()

        # Botón de inicio
        tk.Button(self.frame, text="Iniciar Sesión", command=self.iniciar_sesion, font=("Arial", 14), width=15).pack(pady=30)

    def iniciar_sesion(self):
        usuario = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()

        # Datos de prueba
        if usuario == "admin" and contrasena == "1234":
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

