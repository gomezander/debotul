from core import execute_command, save_output_to_file, clean_url, validar_rango_ip
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime
import re

def execute_masscan(target):
    """
    Ejecuta Masscan para escanear puertos en el target y procesa los resultados en una lista de <IP>:<puerto>.
    """
    # Establecer el tiempo de inicio
    start_time = datetime.now()

    validar_rango_ip(target)

    # Ejecutar Masscan (puertos comunes por defecto)
    command = f"masscan {target} -p21-23,25,80,443,445,8080,8443 --rate=10000"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_masscan'+ RESULTS_FILEEXTENSION, original_target,start_time)
    # Procesar los resultados en una lista de <IP>:<puerto> directamente desde "result"
    
    ip_port_list = []
    for line in result.splitlines():
        # Extraer <IP> y <puerto> usando regex
        match = re.search(r'Discovered open port (\d+)/\w+ on ([\d.]+)', line)
        if match:
            port = match.group(1)
            ip = match.group(2)
            ip_port_list.append(f"{ip}:{port}")

    return ip_port_list