import json
import os

ARCHIVO_JUEGOS = "juegos.json"

class GameManager:
    def __init__(self):
        if not os.path.exists(ARCHIVO_JUEGOS):
            with open(ARCHIVO_JUEGOS, "w") as f:
                json.dump({}, f)

    def cargar_juegos(self):
        with open(ARCHIVO_JUEGOS, "r") as f:
            return json.load(f)

    def guardar_juegos(self, juegos):
        with open(ARCHIVO_JUEGOS, "w") as f:
            json.dump(juegos, f, indent=4)

    def agregar_juego(self, nombre, descripcion):
        juegos = self.cargar_juegos()
        if nombre in juegos:
            return "El juego ya existe."
        juegos[nombre] = {
            "descripcion": descripcion
        }
        self.guardar_juegos(juegos)
        return "OK"

    def eliminar_juego(self, nombre):
        juegos = self.cargar_juegos()
        if nombre in juegos:
            del juegos[nombre]
            self.guardar_juegos(juegos)
            return "OK"
        return "El juego no existe."

    def editar_juego(self, nombre, nueva_descripcion):
        juegos = self.cargar_juegos()
        if nombre in juegos:
            juegos[nombre]["descripcion"] = nueva_descripcion
            self.guardar_juegos(juegos)
            return "OK"
        return "El juego no existe."