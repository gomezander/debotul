# __init__.py

# Puedes importar las funciones principales o clases de cada módulo aquí,
# para que sea más fácil acceder a ellas sin tener que importar el módulo completo.

from core.utils import verificar_servicios_nmap, construir_targets, validar_rango_ip,check_effective_url
from .wpscan import execute_wpscan
from .iis_shortname import execute_iis_shortname
from .masscan import execute_masscan
from .nmap import execute_nmap
from .netexec import execute_netexec
from .enum4linux import execute_enum4linux
from .webanalyze import execute_webanalyze
from .ffuf import execute_ffuf
from .shcheck import execute_shcheck
from .testssl import execute_testssl
from .diablork import execute_diablork
