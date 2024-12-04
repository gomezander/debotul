from core import execute_command, save_output_to_file, clean_url
from core import RESULTS_DIRECTORY, RESULTS_FILEEXTENSION

def execute_testssl(target):
    """
    Ejecuta TestSSL para analizar la configuración TLS/SSL de un servidor.
    """
    
    # Ejecutar TestSSL
    command = f"testssl --protocols --server-defaults -s --connect-timeout 5 --openssl-timeout 5 {target}"
    result = execute_command(command)
    
    original_target = target
    target = clean_url(target)

    # Modificar path para guardar el fichero
    RESULTS_FOLDERPATH = RESULTS_DIRECTORY+'/'+ target+'/'

    # Guardar el resultado en un archivo
    save_output_to_file(result, RESULTS_FOLDERPATH + target+'_testssl'+ RESULTS_FILEEXTENSION, original_target)

    # Restaurar el target original después de Nmap
    target = original_target