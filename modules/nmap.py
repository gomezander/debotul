from core import execute_command, save_output_to_file
from core import LOGS_DIRECTORY, LOG_FILEEXTENSION
import re

def clean_url(target):
    """
    Elimina 'http://' o 'https://' del target si existe.
    """
    return re.sub(r'^https?://', '', target)

def execute_nmap(target):
    """
    Ejecuta Nmap para realizar un escaneo más detallado del target.
    """
    print(f"Iniciando escaneo con Nmap para {target}...")

    # Comprobar si el target tiene http o https y eliminarlo temporalmente
    original_target = target
    if target.startswith("http://") or target.startswith("https://"):
        target = clean_url(target)
    
    # Ejecutar Nmap
    command = f"sudo nmap -sS -p 443,80 {target}"
    result = execute_command(command)
    
    # Modificar path para guardar el fichero
    LOG_FOLDERPATH = LOGS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, LOG_FOLDERPATH + target+'_nmap'+LOG_FILEEXTENSION)

    # Restaurar el target original después de Nmap
    target = original_target