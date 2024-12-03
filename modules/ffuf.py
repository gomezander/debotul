import os
from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION

def execute_ffuf(target):
    """
    Ejecuta FFUF para realizar fuzzing en un sitio web y muestra el progreso por pantalla.
    """

    # Comando para ejecutar FFUF
    command = f"ffuf -u {target}/FUZZ -w ../dependencies/ffuf/test.txt -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'"
    print(f"Ejecutando: {command}")
    print(f"")
    # Ejecutar FFUF y mostrar resultados en tiempo real
    try:
        with os.popen(command) as process:
            output = process.read()
            print(output)  # Mostrar resultados en pantalla
    except Exception as e:
        print(f"Error ejecutando FFUF: {e}")
        return
    original_target = target
    target = clean_url(target)

    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(output, RESULTS_FOLDERPATH + target+'_ffuf'+ RESULTS_FILEEXTENSION)

    # Restaurar el target original después de Nmap
    target = original_target