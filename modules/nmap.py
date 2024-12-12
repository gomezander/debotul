from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime
import re

def execute_nmap(target):
    """
    Ejecuta Nmap para realizar un escaneo más detallado del target.
    """

    # Guardar el target original
    original_target = target

    # Comprobar si el target tiene http o https y eliminarlo temporalmente
    target = clean_url(target)
    
    # Establecer el tiempo de inicio
    start_time = datetime.now()

    # Ejecutar Nmap
    command = f"nmap -Pn -sS --min-rate 10000 --max-retries 3 -p 80,443 {target} -vv"
    result = execute_command(command)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Guardar el resultado en un archivo, pasando start_time para calcular el tiempo transcurrido
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_nmap' + RESULTS_FILEEXTENSION, original_target, start_time)

    # Comprobar si Nmap encontró puertos abiertos
    if not is_ports_open(result):
        print(f"No se encontraron puertos abiertos en {target}. No se ejecutarán más módulos.")
        return False  # Retorna False para indicar que no hay puertos abiertos

    # Restaurar el target original después de Nmap
    target = original_target

    return True  # Retorna True para indicar que Nmap encontró puertos abiertos


def is_ports_open(nmap_result):
    """
    Verifica si Nmap encontró puertos abiertos en el resultado.
    """
    # Buscamos las líneas que contienen 'open' en el resultado de Nmap
    # También se puede buscar en la salida por '80/tcp open' o '443/tcp open', etc.
    open_ports = re.findall(r'\d+/tcp\s+open', nmap_result)

    # Si encontramos al menos una línea que contiene un puerto abierto, devolvemos True
    if open_ports:
        return True
    return False
