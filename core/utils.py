import subprocess
import os
import re
from datetime import datetime
from config import RESULTS_DIRECTORY, TIMEOUT, MAX_RETRIES

def clean_url(target):
    """ 
    Elimina 'http://' o 'https://' y cualquier puerto especificado del target.
    """
    # Eliminar 'http://' o 'https://'
    target = re.sub(r'^https?://', '', target)
    
    # Eliminar el puerto (ejemplo: :8080)
    target = re.sub(r':\d+', '', target)
    
    # Eliminar la barra '/' al final, si está presente
    target = target.rstrip('/')

    return target

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
    Guarda la salida de un comando o el resultado de un módulo en un archivo,
    agregando la fecha y hora de la ejecución.
    """
    try:
        # Obtener la fecha y hora actuales
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Preparar la cabecera con la fecha
        header = f"\n{'='*80}\nFecha de ejecución: {timestamp}\n{'='*80}\n"
        
        # Escribir la cabecera y el resultado en el archivo
        with open(filename, 'a') as file:
            file.write(header)
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
    full_path = os.path.join(RESULTS_DIRECTORY, folder_name)

    try:
        # Crear la carpeta si no existe
        os.makedirs(full_path, exist_ok=True)
        print(f"Carpeta creada en: {full_path}")
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")

    return full_path