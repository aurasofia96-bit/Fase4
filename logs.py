# registro de logs
import logging
import os

# Crear la carpeta 'logs' si no existe
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar el archivo de log
logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def registrar_evento(mensaje):
    """Registra un evento informativo en el log."""
    logging.info(mensaje)

def registrar_error(mensaje):
    """Registra un error controlado en el log."""
    logging.error(mensaje)