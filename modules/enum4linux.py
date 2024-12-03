from core import execute_command, save_output_to_file
from core import LOGS_DIRECTORY

def execute_enum4linux(target):
    """
    Ejecuta Enum4linux para enumerar información de un sistema Windows.
    """
    print(f"Iniciando escaneo con Enum4linux para {target}...")
    
    # Ejecutar Enum4linux
    command = f"enum4linux -a {target}"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, LOGS_DIRECTORY + 'TEST')