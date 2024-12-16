import subprocess
import os
import re
import sys
import ipaddress
from datetime import datetime
from config import RESULTS_DIRECTORY

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

def clean_url(target):
    """ 
    Elimina 'http://' o 'https://', cualquier puerto especificado y el sufijo CIDR (como /16, /24, etc.) del target.
    """
    return re.sub(r'^https?://|:\d+|/$', '', re.sub(r'/\d+', '', target))

def execute_command(command):
    """
    Ejecuta un comando en el sistema operativo y devuelve la salida.
    """
    try:
        print(f"\n{negrita}{azul}----------------------------------------------------------------------------------------------------")
        print(f"                                        Herramienta: {command.split()[0]}                                                  ")
        print(f"{negrita}{azul}----------------------------------------------------------------------------------------------------{reset}")
        print(f"\n{negrita}Ejecutando: {command}{reset}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {command}")
        print(f"Error: {e.stderr.decode('utf-8')}")
        return None

def save_output_to_file(output, filename, target, start_time):
    """
    Guarda la salida de un comando o el resultado de un módulo en un archivo,
    agregando la fecha y hora de la ejecución, sin las secuencias de escape ANSI.
    También agrega el tiempo transcurrido desde el inicio del escaneo.
    """
    try:
        # Eliminar secuencias de escape ANSI (colores y otros formatos)
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)  # Elimina los colores
        output = re.sub(r'\x1b\[[0-9]*K', '', output)  # Elimina el código de borrado de línea [2K
        
        # Obtener la fecha y hora actuales
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Si se proporcionó el tiempo de inicio, calcular el tiempo transcurrido
        if start_time:
            elapsed_time = datetime.now() - start_time
            elapsed_time_str = str(elapsed_time).split('.')[0]  # Eliminar los microsegundos
        else:
            elapsed_time_str = "N/A"  # Si no se proporciona el tiempo de inicio, poner "N/A"
        
        # Preparar la cabecera con la fecha y tiempo transcurrido
        header = f"\n{'='*80}\nFecha de ejecución: {timestamp}\n{'='*80}\nIniciando escaneo para el target: {target}\n"
        header += f"Tiempo transcurrido del escaneo: {elapsed_time_str}\n{'='*80}\n\n\n"
        
        # Escribir la cabecera y el resultado en el archivo
        with open(filename, 'a') as file:
            file.write(header)
            file.write(output + "\n")
    except Exception as e:
        print(f"Error al guardar el archivo {filename}: {str(e)}")

def create_folder(folder_name):
    """
    Crea una carpeta en la ruta especificada.
    """
    folder_name = clean_url(folder_name)

    # Crear la ruta completa
    full_path = os.path.join(RESULTS_DIRECTORY, folder_name)

    try:
        # Crear la carpeta si no existe
        os.makedirs(full_path, exist_ok=True)
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")

    return full_path

def is_valid_ip_or_domain(target):
    """
    Verifica si el input es una IP o un dominio válido.
    """
    # Comprobar si es una IP (IPv4)
    ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ip_regex, target):
        return True

    # Limpiar el dominio antes de validarlo
    target = clean_url(target)

    # Comprobar si es un dominio válido, permitiendo subdominios y guiones
    domain_regex = r'^(?!-)(?!.*-$)(?!.*\.\.)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,}$'
    if re.match(domain_regex, target):
        return True

    return False

# Manejo de Ctrl+C
def signal_handler(sig, frame):
    global interrupted
    print("\nSaliendo de la herramienta...")
    print("\n🔥😈 Diablo ha finalizado. Disfruta de la fruta. 😈🔥\n")
    interrupted = True
    sys.exit(0)

def get_target_from_file(target_file):
    """
    Lee los targets de un archivo.
    """
    with open(target_file, 'r') as file:
        return [line.strip() for line in file.readlines()]

def verificar_servicios_nmap(target, nmap_result):
    """
    Verifica si se encontraron servicios HTTP, HTTPS o SSL/HTTP en el resultado de Nmap.
    
    Args:
        nmap_result (str): Resultado de Nmap como cadena de texto.
        
    Returns:
        list: Lista de puertos encontrados junto con el patrón correspondiente.
    """
    # Expresiones regulares para buscar los servicios http, https o ssl/http
    patrones = [
        (r"(\d+)/tcp\s+open\s+http", 'http'),       # Para http
        (r"(\d+)/tcp\s+open\s+https", 'https'),     # Para https
        (r"(\d+)/tcp\s+open\s+ssl/http", 'ssl/http') # Para ssl/http
    ]
    
    # Usar un set para evitar puertos duplicados, pero manteniendo el protocolo
    puertos_encontrados = {}

    # Buscar las coincidencias en el resultado de Nmap
    for patron, protocolo in patrones:
        coincidencias = re.findall(patron, nmap_result)
        for puerto in coincidencias:
            # Añadir el puerto con su protocolo solo si no está ya en el diccionario
            puertos_encontrados[puerto] = protocolo
    
    # Convertir a lista de tuplas (protocolo, puerto)
    puertos_unicos = [(protocolo, puerto) for puerto, protocolo in puertos_encontrados.items()]
    
       # Pasamos la lista de puertos encontrados a la función construir_targets
    return construir_targets(target, puertos_unicos)


def construir_targets(target, puertos):
    """
    Construye los targets para los puertos encontrados según el servicio (http, https, ssl/http).
    
    Args:
        target (str): El nombre del host o dominio.
        puertos (list): Lista de tuplas con el protocolo y el puerto encontrado.
        
    Returns:
        set: Conjunto de targets construidos.
    """
    # Diccionario para mapear los servicios con sus protocolos
    protocolos = {
        'http': 'http://',
        'https': 'https://',
        'ssl/http': 'https://',  # SSL/HTTP también usa https como protocolo
    }
    
    # Conjunto para almacenar los diferentes targets
    targets = set()
    
    # Construir los targets para cada servicio encontrado
    for protocolo, puerto in puertos:
        if protocolo in protocolos:
            targets.add(f"{protocolos[protocolo]}{target}:{puerto}")

    # Devolver el conjunto de todos los targets construidos
    return targets

def validar_rango_ip(rango_ip):
    try:
        # Intenta crear un objeto IP Network a partir del rango proporcionado
        red = ipaddress.IPv4Network(rango_ip, strict=False)
        return None
    except ValueError:
        return f"El rango {rango_ip} no es válido."
