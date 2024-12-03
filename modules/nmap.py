from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
import re

def execute_nmap(target):
    """
    Ejecuta Nmap para realizar un escaneo más detallado del target.
    """

    # Guardar el target original
    original_target = target

    # Comprobar si el target tiene http o https y eliminarlo temporalmente
    target = clean_url(target)
    
    # Ejecutar Nmap
    command = f"nmap -Pn -sS -sV --min-rate 10000 --max-retries 3 -p 21-25,80,81,443,445,1443,3306,8080,8443 {target} -vv"
    result = execute_command(command)
    
    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_nmap'+RESULTS_FILEEXTENSION)

    # Restaurar el target original después de Nmap
    target = original_target