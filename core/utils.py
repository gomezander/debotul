import subprocess
import os
import re
import sys
from datetime import datetime
from config import RESULTS_DIRECTORY

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

def save_output_to_file(output, filename, target, start_time):
    """
    Guarda la salida de un comando o el resultado de un módulo en un archivo,
    agregando la fecha y hora de la ejecución, sin las secuencias de escape ANSI.
    También agrega el tiempo transcurrido desde el inicio del escaneo.
    """
    try:
        # Eliminar secuencias de escape ANSI (colores y otros formatos)
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)  # Elimina los colores
        output = re.sub(r'\x1b\[[0-9]*K', '', output)  # Elimina el código de borrado de línea [2K
        
        # Obtener la fecha y hora actuales
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Si se proporcionó el tiempo de inicio, calcular el tiempo transcurrido
        if start_time:
            elapsed_time = datetime.now() - start_time
            elapsed_time_str = str(elapsed_time).split('.')[0]  # Eliminar los microsegundos
        else:
            elapsed_time_str = "N/A"  # Si no se proporciona el tiempo de inicio, poner "N/A"
        
        # Preparar la cabecera con la fecha y tiempo transcurrido
        header = f"\n{'='*80}\nFecha de ejecución: {timestamp}\n{'='*80}\nIniciando escaneo para el target: {target}\n"
        header += f"Tiempo transcurrido del escaneo: {elapsed_time_str}\n{'='*80}\n\n\n"
        
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
    folder_name = clean_url(folder_name)

    # Crear la ruta completa
    full_path = os.path.join(RESULTS_DIRECTORY, folder_name)

    try:
        # Crear la carpeta si no existe
        os.makedirs(full_path, exist_ok=True)
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")

    return full_path

def is_valid_ip_or_domain(target):
    """
    Verifica si el input es una IP o un dominio válido.
    """
    # Comprobar si es una IP (IPv4)
    ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ip_regex, target):
        return True

    # Limpiar el dominio antes de validarlo
    target = clean_url(target)

    # Comprobar si es un dominio válido, permitiendo subdominios y guiones
    domain_regex = r'^(?!-)(?!.*-$)(?!.*\.\.)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,}$'
    if re.match(domain_regex, target):
        return True

    return False

# Manejo de Ctrl+C
def signal_handler(sig, frame):
    global interrupted
    print("\nSaliendo de la herramienta...")
    print("\n🔥😈 Diablo ha finalizado. Disfruta de la fruta. 😈🔥\n")
    interrupted = True
    sys.exit(0)

def get_target_from_file(target_file):
    """
    Lee los targets de un archivo.
    """
    with open(target_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def clean_url(target):
    """Elimina 'http://' o 'https://' y otros elementos innecesarios"""
    # Eliminar 'http://' o 'https://'
    target = re.sub(r'^https?://', '', target)
    
    # Eliminar la barra '/' al final, si está presente
    target = target.rstrip('/')

    return target
