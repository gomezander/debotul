from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from core.utils import verificar_servicios_nmap
from datetime import datetime
import re

def execute_nmap(target):
    """
    Ejecuta Nmap para realizar un escaneo más detallado del target y verifica si hay puertos abiertos.
    Si se encuentran puertos abiertos, llama a verificar_servicios_nmap para construir los targets.
    """
    # Guardar el target original
    original_target = target

    # Comprobar si el target tiene http o https y eliminarlo temporalmente
    target = clean_url(target)
    
    # Establecer el tiempo de inicio
    start_time = datetime.now()

    # Ejecutar Nmap
    command = f"nmap -Pn -sS --min-rate 10000 --max-retries 3 -p 80,443,8080,8443 {target} -vv"
    result = execute_command(command)

    # Verificar si Nmap encontró puertos abiertos
    if not is_ports_open(result):
        print(f"No se encontraron puertos abiertos en {target}. Deteniendo ejecución de módulos.")
        return []  # Retorna una lista vacía si no hay puertos abiertos

    # Llamar a verificar_servicios_nmap para obtener los puertos y construir los targets
    targets = verificar_servicios_nmap(target, result)

    if not targets:
        print(f"No se encontraron servicios HTTP/HTTPS/SSL para el target {target}.")
        return []  # Retorna una lista vacía si no se encuentran puertos HTTP/HTTPS

    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'
    
    # Guardar el resultado en un archivo, pasando start_time para calcular el tiempo transcurrido
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_nmap' + RESULTS_FILEEXTENSION, original_target, start_time)

    # Restaurar el target original después de Nmap
    target = original_target

    return targets  # Retorna la lista de targets construidos


def is_ports_open(nmap_result):
    """
    Verifica si Nmap encontró puertos abiertos en el resultado.
    """
    # Buscamos las líneas que contienen 'open' en el resultado de Nmap
    open_ports = re.findall(r'\d+/tcp\s+open', nmap_result)

    # Si encontramos al menos una línea que contiene un puerto abierto, devolvemos True
    return bool(open_ports)
