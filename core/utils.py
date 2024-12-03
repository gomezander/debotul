import subprocess
import os
import re
from config import LOGS_DIRECTORY

def clean_url(target):
    """
    Elimina 'http://' o 'https://' del target si existe.
    """
    return re.sub(r'^https?://', '', target)

def execute_command(command):
    """
    Ejecuta un comando en el sistema operativo y devuelve la salida.
    """
    try:
        print(f"Ejecutando: {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {command}")
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def save_output_to_file(output, filename):
    """
    Guarda la salida de un comando o el resultado de un módulo en un archivo.
    """
    try:
        with open(filename, 'a') as file:
            file.write(output + "\n")
    except Exception as e:
        print(f"Error al guardar el archivo {filename}: {str(e)}")

def create_folder(folder_name):
    """
    Crea una carpeta en la ruta especificada.
    """
    # Comprobar si el target tiene http o https y eliminarlo
    if folder_name.startswith("http://") or folder_name.startswith("https://"):
        folder_name = clean_url(folder_name)

    # Crear la ruta completa
    full_path = os.path.join(LOGS_DIRECTORY, folder_name)

    try:
        # Crear la carpeta si no existe
        os.makedirs(full_path, exist_ok=True)
        print(f"Carpeta creada en: {full_path}")
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")

    return full_path