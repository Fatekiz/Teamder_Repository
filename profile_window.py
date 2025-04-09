import tkinter as tk
from tkinter import messagebox
import json


class ProfileWindow:
    def __init__(self, master, usuario):
        self.master = master
        self.master.title("Tkinter Profile")
        self.master.geometry("400x300")

        self.usuario = usuario

        tk.Button(self.master, text="Ver y Editar Datos de Usuario / Eliminar Cuenta", command=self.ver_datos).pack(pady=10)
        tk.Button(self.master, text="Cerrar Sesion").pack(pady=10)
        tk.Button(self.master, text="Cerrar", command=self.master.destroy).pack(pady=10)



    def ver_datos(self,):
        self.info_profile_window = tk.Toplevel(self.master)
        self.info_profile_window.geometry("400x300")
        self.info_profile_window.title("Ver y Editar Datos de Usuario / Eliminar Cuenta")

        # cargar datos del usuario desde el JSON
        with open("usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        info_usuario = datos.get(self.usuario, {})

        email_actual = info_usuario.get("email", "No registrado")

        # Mostrando los datos de la cuenta
        tk.Label(self.info_profile_window, text=f"Nombre de Usuario: {self.usuario}", font=("Arial", 12)).pack(pady=10)
        tk.Label(self.info_profile_window, text=f"Email: {email_actual}", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.info_profile_window, text="Editar Datos", command=self.editar_datos, font=("Arial",12)).pack(pady=10)

    
    def editar_datos(self):
        self.info_profile_window.withdraw() # Para ocultar la ventana anterior

        #Ventana de verificación de correo
        self.verify_email_window = tk.Toplevel(self.master)
        self.verify_email_window.geometry("500x300")
        self.verify_email_window.title("Verficación de email")

        #ya dentro de la ventana
        tk.Label(self.verify_email_window, text="Ingrese su email (asociado a esta cuenta) para continuar", font=("Arial",12)).pack(pady=10)
        self.entry_email_verify = tk.Entry(self.verify_email_window, font=("Arial",12))
        self.entry_email_verify.pack(pady=10)

        tk.Button(self.verify_email_window, text="Verificar", command=self.verify_email).pack(pady=10)
        tk.Button(self.verify_email_window, text="Cancelar", command=self.verify_email_window.destroy).pack(pady=10)

        # Pagina para editar los datos de la cuenta
        self.edit_profile_window = tk.Toplevel(self.master)
        self.edit_profile_window.geometry("400x300")
        self.edit_profile_window.title("Editar datos de su cuenta")

    
    def verify_email(self):
            email_ingresado = self.entry_email_verify.get()

            with open("usuarios.json", "r") as archivo:
                datos = json.load(archivo)

            email_correcto = datos[self.usuario]["email"]

            if email_ingresado == email_correcto:
                messagebox.showinfo("Exito", "Email verificado correctamente.")
                self.verify_email_window.destroy()
                self.edit_profile_window.destroy()
                self.mostrar_opciones_edicion()
            else:
                messagebox.showerror("Error", "Email incorrecto. Intente nuevamente.")
                self.entry_email_verify.delete(0, tk.END) # Limpiar el campo de entrada
                self.entry_email_verify.focus() # para enfocar nuevamente la ventana ya que se cierra y abre el main_window

    def mostrar_opciones_edicion(self):
            self.edit_profile_window = tk.Toplevel(self.master)
            self.edit_profile_window.geometry("400x300")
            self.edit_profile_window.title("Opciones de Edición")

            tk.Label(self.edit_profile_window, text="Seleccione una opción:", font=("Arial", 12)).pack(pady=20)

            tk.Button(self.edit_profile_window, text="Cambiar Usuario", command=self.cambiar_usuario).pack(pady=5)
            tk.Button(self.edit_profile_window, text="Cambiar Email", command=self.cambiar_email).pack(pady=5)
            tk.Button(self.edit_profile_window, text="Cambiar Contraseña", command=self.cambiar_contraseña).pack(pady=5)
            tk.Button(self.edit_profile_window, text="Eliminar Cuenta", command = self.eliminar_cuenta).pack(pady=5)

    def cambiar_usuario(self):
        self.edit_profile_window.withdraw()

        self.cambiar_usuario_window = tk.Toplevel(self.master)
        self.cambiar_usuario_window.geometry("400x200")
        self.cambiar_usuario_window.title("Cambiar Usuario")

        tk.Label(self.cambiar_usuario_window, text="Ingrese su nuevo nombre de usuario:", font=("Arial", 12)).pack(pady=10)
        self.entry_nuevo_usuario = tk.Entry(self.cambiar_usuario_window, font=("Arial", 12))
        self.entry_nuevo_usuario.pack(pady=10)

        tk.Button(self.cambiar_usuario_window, text="Cambiar", command=self.guardar_nuevo_usuario).pack(pady=10)

    def guardar_nuevo_usuario(self):
        nuevo_usuario = self.entry_nuevo_usuario.get().strip() # strip() hace q elimine espacios en blanco al principio y final

        if not nuevo_usuario:
             messagebox.showerror("Error", "El nombre de usuario no puede estar vacío.")
             return
        
        with open("usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        if nuevo_usuario in datos:
             messagebox.showerror("Error", "El nombre de usuario ya existe.")
             return
        
        # guardar el usuario con el nuevo nombre
        datos[nuevo_usuario] = datos.pop(self.usuario)
        with open("usuarios.json", "w") as archivo:
             json.dump(datos, archivo, indent=4)

        messagebox.showinfo("Éxito", "Nombre de usuario cambiado correctamente. Vuelve a abrir la aplicación para iniciar sesión con el nuevo nombre.")
        self.cambiar_usuario_window.destroy()
        self.master.destroy() # recomendado para que cierre todo e inicie sesion nuevamente con todo compilado otra vez.

    def cambiar_email(self):
        self.edit_profile_window.withdraw()

        self.cambiar_email_window = tk.Toplevel(self.master)
        self.cambiar_email_window.geometry("400x200")
        self.cambiar_email_window.title("Cambiar Email")

        tk.Label(self.cambiar_email_window, text="Ingrese su nuevo email:", font=("Arial", 12)).pack(pady=10)
        self.entry_nuevo_email = tk.Entry(self.cambiar_email_window, font=("Arial", 12))
        self.entry_nuevo_email.pack(pady=10)

        tk.Button(self.cambiar_email_window, text="Cambiar", command=self.guardar_nuevo_email).pack(pady=10)

    def guardar_nuevo_email(self):
        nuevo_email = self.entry_nuevo_email.get().strip()

        if not nuevo_email:
             messagebox.showerror("Error", "El email no puede estar vacío.")
             return
        
        if "@" not in nuevo_email or "." not in nuevo_email:
             messagebox.showerror("Error", "El email no es válido.")
             return
        
        with open("usuarios.json", "r") as archivo:
             datos = json.load(archivo)

        if nuevo_email in [datos[usuario]["email"] for usuario in datos]:
                messagebox.showerror("Error", "El email ya existe.")
                return
        

        datos[self.usuario]["email"] = nuevo_email
        with open("usuarios.json", "w") as archivo:
             json.dump(datos, archivo, indent=4)
        
        messagebox.showinfo("Éxito", "Tu email ha sido actualizado correctamente.(El programa se cerrará para que no tengas problemas!)")
        self.cambiar_email_window.destroy()
        self.master.withdraw()
        self.master.destroy()

    def cambiar_contraseña(self):
        self.edit_profile_window.withdraw()

        self.cambiar_contraseña_window = tk.Toplevel(self.master)
        self.cambiar_contraseña_window.geometry("400x200")
        self.cambiar_contraseña_window.title("Cambiar Contraseña")

        tk.Label(self.cambiar_contraseña_window, text="Ingrese su nueva contraseña:", font=("Arial", 12)).pack(pady=10)
        self.entry_nueva_contraseña = tk.Entry(self.cambiar_contraseña_window, font=("Arial", 12))
        self.entry_nueva_contraseña.pack(pady=10)

        tk.Button(self.cambiar_contraseña_window, text="Cambiar", command=self.guardar_nueva_contraseña).pack(pady=10)

    def guardar_nueva_contraseña(self):
        nueva_contraseña = self.entry_nueva_contraseña.get().strip()

        if not nueva_contraseña:
             messagebox.showerror("Error", "La contraseña no puede estar vacía.")
             return
        
        with open("usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        datos[self.usuario]["clave"] = nueva_contraseña
        with open("usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)

        messagebox.showinfo("Éxito", "Tu contraseña ha sido actualizada correctamente. Vuelve a abrir la aplicación para iniciar sesión con la nueva contraseña.")
        self.cambiar_contraseña_window.destroy()
        self.master.destroy()

    def eliminar_cuenta(self):
        self.edit_profile_window.withdraw()

        self.eliminar_cuenta_window = tk.Toplevel(self.master)
        self.eliminar_cuenta_window.geometry("400x250")
        self.eliminar_cuenta_window.title("Eliminar Cuenta")

        tk.Label(self.eliminar_cuenta_window, text="¿Estás seguro de que deseas eliminar tu cuenta?", font=("Arial", 12)).pack(pady=10)

        tk.Label(self.eliminar_cuenta_window, text="Ingresa tu contraseña para confirmar:", font=("Arial", 10)).pack(pady=5)
        self.entry_confirmar_clave = tk.Entry(self.eliminar_cuenta_window, show="*", font=("Arial", 12))
        self.entry_confirmar_clave.pack(pady=5)

        tk.Button(self.eliminar_cuenta_window, text="Eliminar", command=self.confirmar_eliminar).pack(pady=10)
        tk.Button(self.eliminar_cuenta_window, text="Cancelar", command=self.eliminar_cuenta_window.destroy).pack(pady=5)


    def confirmar_eliminar(self):
        clave_ingresada = self.entry_confirmar_clave.get()

        with open("usuarios.json", "r") as archivo:
            datos = json.load(archivo)

        if self.usuario not in datos:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        clave_real = datos[self.usuario]["clave"]

        if clave_ingresada != clave_real:
            messagebox.showerror("Error", "Contraseña incorrecta. No se pudo eliminar la cuenta.")
            return

        # Si la contraseña coincide, eliminamos la cuenta
        del datos[self.usuario]

        with open("usuarios.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)

        messagebox.showinfo("Cuenta eliminada", "Tu cuenta ha sido eliminada correctamente.")
        self.eliminar_cuenta_window.destroy()
        self.master.destroy()
