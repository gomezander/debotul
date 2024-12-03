from core import execute_command, save_output_to_file
from core import LOGS_DIRECTORY

def execute_ffuf(target):
    """
    Ejecuta FFUF para realizar fuzzing en un sitio web.
    """
    print(f"Iniciando escaneo con FFUF para {target}...")
    
    # Ejecutar FFUF (puedes personalizar los parámetros según necesidades)
    command = f"ffuf -u {target}/FUZZ -w /path/to/wordlist.txt"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, LOGS_DIRECTORY + 'TEST')