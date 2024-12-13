from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

def execute_shcheck(target):
    """
    Ejecuta shcheck para validar configuraciones HTTP/HTTPS en el target.
    """

    # Establecer el tiempo de inicio
    start_time = datetime.now()

    # Comprobar si el target tiene http:// o https://
    command = f"shcheck.py -d {target}"
    result = execute_command(command)
    save_results(result, target, target, start_time)


def save_results(result, target, full_target, start_time):
    """
    Guarda los resultados del comando shcheck.
    """
    # Limpiar el target (eliminar http:// o https://)
    original_target = target
    target = clean_url(target)

    # Modificar el path para guardar el archivo de resultados
    LOG_FOLDERPATH = RESULTS_DIRECTORY + '/' + target + '/'

    # Guardar el resultado en el archivo adecuado, añadiendo el tiempo transcurrido
    save_output_to_file(result,LOG_FOLDERPATH + target + '_shcheck' + RESULTS_FILEEXTENSION, full_target,start_time)

    # Restaurar el target original después de procesar
    target = original_target