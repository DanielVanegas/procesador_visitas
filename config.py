import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Rutas principales
BASE_DIR = os.path.expanduser("~/servidor_avaluos/montaje/pendientes")
INSUMOS_DIR = os.path.expanduser("~/servidor_avaluos/insumos/parametros")

# Buscar el único archivo .xlsx en la carpeta de parámetros
def encontrar_param_file():
    for archivo in os.listdir(INSUMOS_DIR):
        if archivo.endswith(".xlsx"):
            return os.path.join(INSUMOS_DIR, archivo)
    raise FileNotFoundError("No se encontró ningún archivo .xlsx en la carpeta de parámetros.")

PARAM_FILE_PATH = encontrar_param_file()

# Configuración base de datos
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', 5432)
}
