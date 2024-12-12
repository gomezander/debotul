import os
from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_testssl(target):
    """
    Ejecuta TestSSL para analizar la configuración TLS/SSL de un servidor.
    """

    # Comprobar si el target tiene http:// o https://
    if target.startswith("http://"):
        print(f"El target {target} ya tiene el protocolo HTTP, no se ejecutará TestSSL.")
        return  # Si ya tiene http://, no hace nada

    elif target.startswith("https://"):
        print(f"Ejecutando TestSSL con el target HTTPS: {target}")
        # Si tiene https://, ejecutamos TestSSL directamente
        run_testssl(target)

    else:
        # Si el target no tiene http:// ni https://, comprobamos Nmap
        nmap_file = f"../results/{target}/{target}_nmap.txt"
        
        if os.path.exists(nmap_file):
            with open(nmap_file, 'r') as file:
                nmap_output = file.read()
            
            # Verificar si el puerto 443 (HTTPS) está abierto
            if "Discovered open port 443/tcp" in nmap_output:
                print(f"El puerto 443 (HTTPS) está abierto en {target}. Ejecutando TestSSL con HTTPS.")
                https_target = f"https://{target}"
                run_testssl(https_target)
            else:
                print(f"No se encontró el puerto 443 abierto en el archivo de Nmap para {target}. No se ejecuta TestSSL.")
        else:
            print(f"No se encontró el archivo de Nmap para {target}. No se ejecuta TestSSL.")

def run_testssl(target):
    """Ejecuta TestSSL con la URL proporcionada y guarda el tiempo transcurrido"""

    # Establecer el tiempo de inicio
    start_time = datetime.now()

    # Ejecutar TestSSL
    command = f"testssl --protocols --server-defaults -s --connect-timeout 5 --openssl-timeout 5 {target}"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)

    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Guardar el resultado en un archivo, añadiendo el tiempo transcurrido
    save_output_to_file(result,RESULTS_FOLDERPATH + target + '_testssl' + RESULTS_FILEEXTENSION, original_target,start_time)

    # Restaurar el target original después de la ejecución
    target = original_target
