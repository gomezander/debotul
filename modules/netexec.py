from core import execute_command, save_output_to_file
from core import RESULTS_DIRECTORY

def execute_netexec(target):
    """
    Ejecuta Netexec para obtener información sobre la red SMB en el target.
    """
    
    # Ejecutar Netexec (comando SMB)
    command = f"netexec {target}"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_DIRECTORY + 'test')