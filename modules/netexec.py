from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_netexec(target):
    """
    Ejecuta Netexec para obtener información sobre la red SMB en el target.
    """
    # Establecer el tiempo de inicio
    start_time = datetime.now()

    original_target = target
    target = clean_url(target)

    # Ejecutar Netexec (comando SMB)
    command = f"netexec smb {target} -u '' -p '' --shares"
    result = execute_command(command)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_netexec'+ RESULTS_FILEEXTENSION, target,start_time)

    # Restaurar el target original después de _enum4linux
    target = original_target