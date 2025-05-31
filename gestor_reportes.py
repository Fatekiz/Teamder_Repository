import json
import os

ARCHIVO_REPORTES = "reportes.json"

def cargar_reportes():
    if not os.path.exists(ARCHIVO_REPORTES):
        return []
    with open(ARCHIVO_REPORTES, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_reportes(reportes):
    with open(ARCHIVO_REPORTES, "w", encoding="utf-8") as f:
        json.dump(reportes, f, indent=4)

def agregar_reporte(usuario, titulo, descripcion):
    reportes = cargar_reportes()
    nuevo_reporte = {
        "usuario": usuario,
        "titulo": titulo,
        "descripcion": descripcion,
        "estado": "Pendiente"
    }
    reportes.append(nuevo_reporte)
    guardar_reportes(reportes)

def actualizar_estado(indice, nuevo_estado):
    reportes = cargar_reportes()
    if 0 <= indice < len(reportes):
        reportes[indice]["estado"] = nuevo_estado
        guardar_reportes(reportes)
        return True
    return False

def eliminar_reporte(indice):
    reportes = cargar_reportes()
    if 0 <= indice < len(reportes):
        reportes.pop(indice)
        guardar_reportes(reportes)
        return True
    return False
