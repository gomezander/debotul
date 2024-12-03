from core import execute_command, save_output_to_file
from core import LOGS_DIRECTORY, LOG_FILEEXTENSION
import re

def clean_url(target):
    """
    Elimina 'http://' o 'https://' del target si existe.
    """
    return re.sub(r'^https?://', '', target)

def execute_testssl(target):
    """
    Ejecuta TestSSL para analizar la configuración TLS/SSL de un servidor.
    """
    print(f"Iniciando escaneo con TestSSL para {target}...")
    
    # Ejecutar TestSSL
    command = f"testssl --protocols --server-defaults -s --connect-timeout 5 --openssl-timeout 5 {target}"
    result = execute_command(command)

    # Comprobar si el target tiene http o https y eliminarlo temporalmente
    original_target = target
    if target.startswith("http://") or target.startswith("https://"):
        target = clean_url(target)
    
    # Modificar path para guardar el fichero
    LOG_FOLDERPATH = LOGS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, LOG_FOLDERPATH + target+'_testssl'+LOG_FILEEXTENSION)

    # Restaurar el target original después de Nmap
    target = original_target