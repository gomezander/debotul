from core import execute_command, save_output_to_file, clean_url,check_effective_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from modules import execute_iis_shortname, execute_wpscan   
from datetime import datetime

def execute_webanalyze(target):
    """
    Ejecuta Webanalyze para detectar las tecnologías utilizadas por la web.
    """
    # Guardar el target original
    original_target = target

    # Establecer el tiempo de inicio
    start_time = datetime.now()

    effective_target = check_effective_url(target)

    # Asegurar que la URL tenga una barra al final específicamente para FFUF
    if not target.endswith('/'):
        target_with_slash = target + '/'
    else:
        target_with_slash = target

    if effective_target == target_with_slash:
    # Ejecutar Webanalyze
        command = f"webanalyze -apps ../dependencies/webanalyze/technologies.json -host {target}"
        result = execute_command(command)

        target = clean_url(target)

        # Modificar path para guardar el fichero
        RESULTS_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

        # Guardar el resultado en un archivo, añadiendo el tiempo transcurrido
        save_output_to_file(result,RESULTS_FOLDERPATH + target + '_webanalyze' + RESULTS_FILEEXTENSION, original_target, start_time)

        # Restaurar el target original después de Webanalyze
        target = original_target

        # Analizar el resultado para decidir si ejecutar IIS Shortname
        if "IIS" in result:
            print("Microsoft-IIS detectado. Ejecutando IIS Shortname Scan...")
            execute_iis_shortname(target)
        else:
            pass
        
        # Analizar el resultado para decidir si ejecutar WPScan
        if "WordPress" in result:
            print("WordPress detectado. Ejecutando WPScan...")
            execute_wpscan(target)
        else:
            pass