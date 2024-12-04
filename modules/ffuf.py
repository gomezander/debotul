import os
from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION

def execute_ffuf(target):
    """
    Ejecuta FFUF para realizar fuzzing en un sitio web y muestra el progreso por pantalla.
    """

    # Asegurar que la URL tenga una barra al final específicamente para FFUF
    if not target.endswith('/'):
        target_with_slash = target + '/'
    else:
        target_with_slash = target

    # Comando para ejecutar FFUF
    command = f"ffuf -u {target_with_slash}FUZZ -w ../dependencies/ffuf/test.txt -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'"
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
    save_output_to_file(output, RESULTS_FOLDERPATH + target+'_ffuf'+ RESULTS_FILEEXTENSION, original_target)

    # Restaurar el target original después de ffuf
    target = original_target