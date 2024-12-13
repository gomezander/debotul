from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from modules import execute_iis_shortname
from datetime import datetime

def execute_webanalyze(target):
    """
    Ejecuta Webanalyze para detectar las tecnologías utilizadas por la web.
    """
    # Guardar el target original
    original_target = target

    # Establecer el tiempo de inicio
    start_time = datetime.now()

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
        print("Microsoft-IIS no detectado. Omitiendo IIS Shortname Scan.")
