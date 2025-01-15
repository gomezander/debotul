from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

# Definir códigos de escape ANSI para negrita y colores
negrita = "\033[1m"
rojo = "\033[91m"
verde = "\033[92m"
amarillo = "\033[93m"
azul = "\033[94m"
magenta = "\033[95m"
cyan = "\033[96m"
blanco = "\033[97m"
reset = "\033[0m"

def execute_testssl(target):
    """
    Ejecuta TestSSL para analizar la configuración TLS/SSL de un servidor.
    """

    # Comprobar si el target tiene http:// o https://
    if target.startswith("http://"):
        return  # Si ya tiene http://, no hace nada

    else: 
        target.startswith("https://")
        # Si tiene https://, ejecutamos TestSSL directamente
        run_testssl(target)


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
    
    # Guardar el resultado en un archivo, pasando start_time para calcular el tiempo transcurrido
    save_output_to_file(result, RESULTS_FOLDERPATH + target + '_testssl' + RESULTS_FILEEXTENSION, original_target, start_time)

    # Restaurar el target original después de Nmap
    target = original_target

