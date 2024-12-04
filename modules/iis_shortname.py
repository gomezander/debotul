from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION

def execute_iis_shortname(target):
    """
    Ejecuta un escaneo para obtener los nombres cortos de archivos en IIS.
    """
    
    # Ejecutar IIS ShortName Scan (este comando puede necesitar adaptarse)
    command = f"shortscan {target}"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_shortscan'+ RESULTS_FILEEXTENSION)

    # Restaurar el target original después de iis_shortname
    target = original_target