from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION

def execute_enum4linux(target):
    """
    Ejecuta Enum4linux para enumerar información de un sistema Windows.
    """
    
    # Ejecutar Enum4linux
    command = f"enum4linux -a {target}"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_DIRECTORY + RESULTS_FILEEXTENSION)