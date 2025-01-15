# __init__.py

# Puedes importar las funciones principales de cada módulo aquí,
# para simplificar las importaciones en otros archivos del proyecto.

from .config import RESULTS_DIRECTORY, TIMEOUT, MAX_RETRIES, RESULTS_FILEEXTENSION
from .menu import show_menu
from .utils import execute_command, save_output_to_file, clean_url,is_valid_ip_or_domain,signal_handler,get_target_from_file,validar_rango_ip,check_effective_url