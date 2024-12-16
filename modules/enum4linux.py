from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_enum4linux(target):
    """
    Ejecuta Enum4linux para enumerar información de un sistema Windows.
    """
    # Establecer el tiempo de inicio
    start_time = datetime.now()

    original_target = target
    target = clean_url(target)

    # Ejecutar Enum4linux
    command = f"enum4linux -a {target}"
    result = execute_command(command)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_enum4linux'+ RESULTS_FILEEXTENSION, target,start_time)

    # Restaurar el target original después de _enum4linux
    target = original_target