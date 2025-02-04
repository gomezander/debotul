import os
import subprocess
import re
from core import save_output_to_file, clean_url,check_effective_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION
from datetime import datetime

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

def execute_ffuf(target):
    """
    Ejecuta FFUF para realizar fuzzing en un sitio web y guarda únicamente los resultados encontrados.
    """
    start_time = datetime.now()

    effective_target = check_effective_url(target)
    
    # Asegurar que la URL tenga una barra al final específicamente para FFUF
    if not target.endswith('/'):
        target_with_slash = target + '/'
    else:
        target_with_slash = target

    if effective_target == target_with_slash:

        # Verificar si el target tiene http:// o https://
        target_with_slash = effective_target if effective_target.endswith('/') else effective_target + '/'

        # Ejecutar FFUF con el protocolo elegido
        print(target_with_slash)
        run_ffuf(target_with_slash, target, start_time)

def run_ffuf(target_with_slash, original_target, start_time):
    """Ejecuta FFUF con la URL proporcionada"""
    # Comando para ejecutar FFUF
    command = [
        "ffuf",
        "-u", f"{target_with_slash}FUZZ",
        "-w", "../dependencies/ffuf/test.txt",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "-c",
        "-ac"
    ]

    print(f"\n{negrita}{azul}----------------------------------------------------------------------------------------------------")
    print(f"                                        Herramienta: ffuf                                                  ")
    print(f"{negrita}{azul}----------------------------------------------------------------------------------------------------{reset}")
    print(f"\n{negrita}Ejecutando: {command}{reset}")

    # Ejecutar FFUF y capturar únicamente los resultados encontrados
    try:
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
            output = ""
            relevant_lines = []
            for line in process.stdout:
                print(line, end="")  # Mostrar cada línea en pantalla en tiempo real
                output += line

                # Comprobar la condición de duración y solicitudes por segundo
                if "Duration:" in line and "req/sec" in line:
                    duration_match = re.search(r"Duration: \[(\d+:\d+:\d+)\]", line)
                    req_sec_match = re.search(r"(\d+) req/sec", line)

                    if duration_match and req_sec_match:
                        duration = duration_match.group(1)
                        req_sec = int(req_sec_match.group(1))

                        # Convertir duración a segundos para comparación
                        h, m, s = map(int, duration.split(":"))
                        total_seconds = h * 3600 + m * 60 + s

                        if total_seconds >= 2 and 0 <= req_sec <= 20:
                            print("\nSaturación del servidor. Deteniendo FFUF y continuando con el siguiente módulo.")
                            # Limpiar y guardar los resultados
                            target = clean_url(original_target)
                            RESULTS_FOLDERPATH = os.path.join(RESULTS_DIRECTORY, target)
                            os.makedirs(RESULTS_FOLDERPATH, exist_ok=True)

                            # Guardar únicamente los resultados relevantes en un archivo
                            output_file_path = os.path.join(RESULTS_FOLDERPATH, f"{target}_ffuf{RESULTS_FILEEXTENSION}")
                            save_output_to_file("".join(relevant_lines), output_file_path, original_target, start_time)
                            original_target = target
                            process.terminate()
                            return

                # Filtrar líneas relevantes con resultados encontrados
                if any(keyword in line for keyword in ["[Status:", "[Size:", "[Words:", "[Lines:"]):
                    relevant_lines.append(line)
    except Exception as e:
        print(f"Error ejecutando FFUF: {e}")
        return

    # Limpiar y guardar los resultados
    target = clean_url(original_target)
    RESULTS_FOLDERPATH = os.path.join(RESULTS_DIRECTORY, target)
    os.makedirs(RESULTS_FOLDERPATH, exist_ok=True)

    # Guardar únicamente los resultados relevantes en un archivo
    output_file_path = os.path.join(RESULTS_FOLDERPATH, f"{target}_ffuf{RESULTS_FILEEXTENSION}")
    save_output_to_file("".join(relevant_lines), output_file_path, original_target, start_time)

    original_target = target
