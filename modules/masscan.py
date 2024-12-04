from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION

def execute_masscan(target):
    """
    Ejecuta Masscan para escanear puertos en el target.
    """
    
    # Ejecutar Masscan (puertos comunes por defecto)
    command = f"masscan {target} -p80,443,8080 --rate=10000"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_DIRECTORY + 'test')