from core import execute_command, save_output_to_file, clean_url, validar_rango_ip
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime
import re

def execute_masscan(target):
    """
    Ejecuta Masscan para escanear puertos en el target y procesa los resultados.
    Crea un archivo con todos los resultados y otro con las IPs con puertos específicos abiertos.
    """

    filtered_ports = {80, 443, 8080, 8443}

    # Establecer el tiempo de inicio
    start_time = datetime.now()

    validar_rango_ip(target)

    # Ejecutar Masscan (puertos comunes por defecto)
    command = f"masscan {target} -p21-23,25,80,443,445,1433,1521,3306,5432,8080,8443 --rate=10000"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'
    
    filtered_results_file = RESULTS_FOLDERPATH + target + '_filtered_ips' + RESULTS_FILEEXTENSION

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_masscan'+ RESULTS_FILEEXTENSION, original_target,start_time)
    # Procesar los resultados en una lista de <IP>:<puerto> directamente desde "result"
    
    ip_port_list = []
    filtered_ips = [] 

    for line in result.splitlines():
        # Extraer <IP> y <puerto> usando regex
        match = re.search(r'Discovered open port (\d+)/\w+ on ([\d.]+)', line)
        if match:
            port = match.group(1)
            ip = match.group(2)
            ip_port_list.append(f"{ip}:{port}")

            # Añadir la URL correspondiente al puerto y la IP si es uno de los filtrados
            if port in filtered_ports:
                if port == 80:
                    filtered_ips.append(f"http://{ip}:{port}")
                elif port == 443:
                    filtered_ips.append(f"https://{ip}:{port}")
                elif port == 8080:
                    filtered_ips.append(f"http://{ip}:{port}")
                elif port == 8443:
                    filtered_ips.append(f"https://{ip}:{port}")

    # Guardar las URLs filtradas en el archivo
    with open(filtered_results_file, 'w') as f:
        f.write("\n".join(filtered_ips))

    return ip_port_list