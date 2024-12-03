from core import execute_command, save_output_to_file
from core import LOGS_DIRECTORY

def execute_masscan(target):
    """
    Ejecuta Masscan para escanear puertos en el target.
    """
    print(f"Iniciando escaneo con Masscan para {target}...")
    
    # Ejecutar Masscan (puertos comunes por defecto)
    command = f"masscan {target} -p80,443,8080 --rate=10000"
    result = execute_command(command)
    
    # Guardar el resultado en un archivo
    save_output_to_file(result, LOGS_DIRECTORY + 'TEST')