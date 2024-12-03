from core import execute_command, save_output_to_file
from core import LOGS_DIRECTORY

def execute_netexec(target):
    """
    Ejecuta Netexec para obtener información sobre la red SMB en el target.
    """
    print(f"Iniciando escaneo con Netexec para {target}...")
    
    # Ejecutar Netexec (comando SMB)
    command = f"netexec {target}"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, LOGS_DIRECTORY + 'TEST')