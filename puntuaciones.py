import json
import os

NOMBRE_ARCHIVO = "record.json"

def cargar_puntuacion_maxima():
    """Lee el puntaje más alto desde el archivo JSON."""
    if not os.path.exists(NOMBRE_ARCHIVO):
        return 0  # Si el archivo no existe, el récord es 0
    
    try:
        with open(NOMBRE_ARCHIVO, "r") as archivo:
            datos = json.load(archivo)
            return datos.get("max_puntuacion", 0)
    except (json.JSONDecodeError, IOError):
        return 0

def guardar_puntuacion_maxima(nueva_puntuacion):
    """Guarda el nuevo récord en el archivo JSON."""
    datos = {"max_puntuacion": nueva_puntuacion}
    try:
        with open(NOMBRE_ARCHIVO, "w") as archivo:
            json.dump(datos, archivo)
    except IOError as e:
        print(f"Error al guardar el récord: {e}")