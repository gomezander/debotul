from core import execute_command, save_output_to_file, clean_url, validar_rango_ip
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_masscan(target):
    """
    Ejecuta Masscan para escanear puertos en el target.
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

    # Restaurar el target original después de masscan
    target = original_target