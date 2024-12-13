from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_wpscan(target):
    """
    Ejecuta un escaneo para obtener información del WordPress
    """
    # Establecer el tiempo de inicio
    start_time = datetime.now()
    
    # Ejecutar WPscan Scan (este comando puede necesitar adaptarse)
    command = f" wpscan --url {target} --enumerate p --random-user-agent --throttle 5 --plugins-detection passive --plugins-version-detection passive --detection-mode passive --request-timeout 10 --connect-timeout 10 --disable-tls-checks {target}"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_wpscan'+ RESULTS_FILEEXTENSION, original_target,start_time)

    # Restaurar el target original después de WPScan
    target = original_target