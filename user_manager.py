import json
import os
import re

ARCHIVO_USUARIOS = "usuarios.json"

class UserManager:
    def __init__(self):
        self.usuarios = self.cargar_usuarios()
        if not os.path.exists(ARCHIVO_USUARIOS):
            with open(ARCHIVO_USUARIOS, "w") as f:
                json.dump({}, f)

    def cargar_usuarios(self):
        with open(ARCHIVO_USUARIOS, "r") as f:
            return json.load(f)

    def guardar_usuarios(self, usuarios):
        with open(ARCHIVO_USUARIOS, "w") as f:
            json.dump(usuarios, f, indent=4)

    def es_email_valido(self, email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email)

    def registrar(self, usuario, email, clave):
        usuarios = self.cargar_usuarios()

        if usuario in usuarios:
            return "Usuario ya existe"
        if not self.es_email_valido(email):
            return "Email inválido"

        usuarios[usuario] = {
            "email": email,
            "clave": clave
        }

        self.guardar_usuarios(usuarios)
        return "OK"

    def verificar_login(self, usuario, clave):
        usuarios = self.cargar_usuarios()
        return usuario in usuarios and usuarios[usuario]["clave"] == clave

    def es_admin(self, usuario):
        return self.usuarios.get(usuario, {}).get("admin", False)