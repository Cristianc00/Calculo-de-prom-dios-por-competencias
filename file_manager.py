# file_manager.py
import json

def guardar_competencias_json(file_path, data):
    """Guarda la estructura de competencias en un archivo JSON."""
    try:
        with open(file_path, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, ensure_ascii=False, indent=4)
        return True, None  # Éxito
    except Exception as e:
        return False, e  # Error

def cargar_competencias_json(file_path):
    """Carga la estructura de competencias desde un archivo JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, None  # Éxito
    except Exception as e:
        return None, e  # Error

def guardar_promedios_csv(file_path, alumnos):
    """Guarda la lista de alumnos y promedios en formato CSV."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Alumno,Promedio\n")
            for alumno in alumnos:
                f.write(f"{alumno['nombre']},{alumno['promedio']:.2f}\n")
        return True, None
    except Exception as e:
        return False, e

def guardar_promedios_txt(file_path, alumnos):
    """Guarda la lista de alumnos y promedios en formato TXT."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for alumno in alumnos:
                f.write("----- RESULTADO -----\n")
                f.write(f"Alumno: {alumno['nombre']}\n")
                f.write(f"Promedio: {alumno['promedio']:.2f}\n")
                f.write("---------------------\n")
        return True, None
    except Exception as e:
        return False, e