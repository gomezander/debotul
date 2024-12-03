from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
import re

def execute_shcheck(target):
    """
    Ejecuta shcheck para validar configuraciones HTTP/HTTPS en el target.
    """

    # Comprobar si el target tiene http o https
    if target.startswith("http://") or target.startswith("https://"):
        command = f"shcheck.py -d {target}"
        print(f"Ejecutando shcheck con esquema existente: {target}")
        result = execute_command(command)
        save_results(result,target)
    else:
        # Ejecutar shcheck con http
        http_target = f"http://{target}"
        print(f"Ejecutando shcheck con HTTP: {http_target}")
        http_result = execute_command(f"shcheck.py -d {http_target}")

        # Modificar path para guardar el fichero
        LOG_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

        save_output_to_file(http_result, LOG_FOLDERPATH + target+'_shcheck'+RESULTS_FILEEXTENSION)

        # Ejecutar shcheck con https
        https_target = f"https://{target}"
        print(f"Ejecutando shcheck con HTTPS: {https_target}")
        https_result = execute_command(f"shcheck.py -d {https_target}")

        # Modificar path para guardar el fichero
        LOG_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

        save_output_to_file(https_result, LOG_FOLDERPATH + target+'_shcheck'+RESULTS_FILEEXTENSION)

def save_results (result, target):
    # Comprobar si el target tiene http o https y eliminarlo temporalmente
    original_target = target
    target = clean_url(target)

    # Modificar path para guardar el fichero
    LOG_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    save_output_to_file(result, LOG_FOLDERPATH + target+'_shcheck'+RESULTS_FILEEXTENSION)