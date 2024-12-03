# __init__.py

# Puedes importar las funciones principales o clases de cada módulo aquí,
# para que sea más fácil acceder a ellas sin tener que importar el módulo completo.

from .masscan import execute_masscan
from .nmap import execute_nmap
from .netexec import execute_netexec
from .enum4linux import execute_enum4linux
from .iis_shortname import execute_iis_shortname
from .webanalyze import execute_webanalyze
from .ffuf import execute_ffuf
from .shcheck import execute_shcheck
from .testssl import execute_testssl