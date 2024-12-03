from core import execute_command, save_output_to_file
from core import RESULTS_DIRECTORY

def execute_iis_shortname(target):
    """
    Ejecuta un escaneo para obtener los nombres cortos de archivos en IIS.
    """
    
    # Ejecutar IIS ShortName Scan (este comando puede necesitar adaptarse)
    command = f"iis-shortname-scan {target}"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_DIRECTORY + 'test')