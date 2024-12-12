import os
import sys
import signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import execute_masscan
from modules import execute_nmap
from modules import execute_netexec
from modules import execute_enum4linux
from modules import execute_webanalyze
from modules import execute_ffuf
from modules import execute_shcheck
from modules import execute_testssl
from utils import create_folder,is_valid_ip_or_domain,signal_handler,get_target_from_file
from menu import show_menu
from config import RESULTS_DIRECTORY, TIMEOUT, MAX_RETRIES

# Variable global para manejar la interrupción del programa (Ctrl+C)
interrupted = False

# Configurar la señal para Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def run_profile(profile, targets):
    """
    Ejecuta el perfil de escaneo seleccionado por el usuario secuencialmente.
    """
    for target in targets:
        create_folder(target)
        print(f"\nIniciando escaneo para el target: {target}")

        if profile == "HTTP":
            # Primero ejecutamos Nmap
            if not execute_nmap(target):
                continue  # Si Nmap no encontró puertos abiertos, pasamos al siguiente target

            modules = [
                execute_webanalyze,
                execute_shcheck,
                execute_testssl,
                execute_ffuf
            ]
        else:
            print("Perfil no reconocido. Omitiendo...")
            continue

        # Ejecutar módulos secuencialmente
        for module in modules:
            if interrupted:
                break
            module(target)

def main():
    """
    Función principal de la herramienta que gestiona la interacción con el usuario
    y la ejecución de los módulos.
    """
    print("Bienvenido a DiabloX\n")

    # Verificar si el usuario proporcionó un archivo de target o una URL/IP
    if len(sys.argv) < 2:
        print("Por favor, proporcione un archivo con targets o una URL/IP como argumento.")
        sys.exit(1)

    target_input = sys.argv[1]

    # Comprobar si el input es un archivo o una URL/IP
    if os.path.isfile(target_input):
        targets = get_target_from_file(target_input)
    else:
        targets = [target_input]

    # Validar si los targets son IPs o dominios válidos
    valid_targets = []
    for target in targets:
        if is_valid_ip_or_domain(target):
            valid_targets.append(target)
        else:
            print(f"Advertencia: '{target}' no es una IP o dominio válido. Se omitirá.")

    if not valid_targets:
        print("No se encontraron targets válidos. El programa se detendrá.")
        sys.exit(1)

    # Mostrar el menú una sola vez y solicitar elección del perfil
    profile = show_menu()

    if profile == "Exit":
        print("Saliendo de la herramienta...")
    elif profile:
        run_profile(profile, valid_targets)
    else:
        print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
