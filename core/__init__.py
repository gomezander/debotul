# __init__.py

# Puedes importar las funciones principales de cada módulo aquí,
# para simplificar las importaciones en otros archivos del proyecto.

from .config import RESULTS_DIRECTORY, TIMEOUT, MAX_RETRIES, RESULTS_FILEEXTENSION
from .menu import show_menu
from .utils import execute_command, save_output_to_file, clean_url,is_valid_ip_or_domain,signal_handler,get_target_from_file

# Definir códigos de escape ANSI para negrita y colores
negrita = "\033[1m"
rojo = "\033[91m"
verde = "\033[92m"
amarillo = "\033[93m"
azul = "\033[94m"
magenta = "\033[95m"
cyan = "\033[96m"
blanco = "\033[97m"
reset = "\033[0m"