from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
import re
import os
from datetime import datetime

def execute_shcheck(target):
    """
    Ejecuta shcheck para validar configuraciones HTTP/HTTPS en el target.
    """

    # Establecer el tiempo de inicio
    start_time = datetime.now()

    # Comprobar si el target tiene http:// o https://
    if target.startswith("http://") or target.startswith("https://"):
        command = f"shcheck.py -d {target}"
        result = execute_command(command)
        save_results(result, target, target, start_time)
    else:
        # Comprobar el archivo de Nmap para determinar qué puertos están abiertos
        nmap_file = f"../results/{target}/{target}_nmap.txt"
        
        if os.path.exists(nmap_file):
            with open(nmap_file, 'r') as file:
                nmap_output = file.read()
            
            # Verificar si los puertos 80 y 443 están abiertos
            http_found = "Discovered open port 80/tcp" in nmap_output
            https_found = "Discovered open port 443/tcp" in nmap_output

            if http_found and https_found:
                # Si ambos puertos están abiertos, ejecutar shcheck para ambos
                targets_to_check = [f"http://{target}", f"https://{target}"]
            elif http_found:
                # Si solo el puerto 80 está abierto, ejecutar shcheck con http
                targets_to_check = [f"http://{target}"]
            elif https_found:
                # Si solo el puerto 443 está abierto, ejecutar shcheck con https
                targets_to_check = [f"https://{target}"]
            else:
                print(f"No se encontró puerto 80 o 443 abiertos en el archivo de Nmap para {target}")
                return
        else:
            print(f"No se encontró el archivo de Nmap para {target}")
            return

        # Ejecutar shcheck para cada uno de los targets correspondientes
        for target_url in targets_to_check:
            result = execute_command(f"shcheck.py -d {target_url}")
            save_results(result, target, target_url, start_time)

def save_results(result, target, full_target, start_time):
    """
    Guarda los resultados del comando shcheck.
    """
    # Limpiar el target (eliminar http:// o https://)
    original_target = target
    target = clean_url(target)

    # Modificar el path para guardar el archivo de resultados
    LOG_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Guardar el resultado en el archivo adecuado, añadiendo el tiempo transcurrido
    save_output_to_file(result,LOG_FOLDERPATH + target + '_shcheck' + RESULTS_FILEEXTENSION, full_target,start_time)

    # Restaurar el target original después de procesar
    target = original_target
