from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from modules import execute_iis_shortname

def execute_webanalyze(target):
    """
    Ejecuta Webanalyze para detectar las tecnologías utilizadas por la web.
    """
    
    # Ejecutar Webanalyze
    command = f"webanalyze -apps ../dependencies/webanalyze/technologies.json -host {target}"
    result = execute_command(command)

    original_target = target
    target = clean_url(target)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_webanalyze'+ RESULTS_FILEEXTENSION)

    # Restaurar el target original después de Nmap
    target = original_target

    # Analizar el resultado para decidir si ejecutar IIS Shortname
    if "IIS" in result:
        print("Microsoft-IIS detectado. Ejecutando IIS Shortname Scan...")
        execute_iis_shortname(target)
    else:
        print("Microsoft-IIS no detectado. Omitiendo IIS Shortname Scan.")