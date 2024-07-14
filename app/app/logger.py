# logger.py
import logging
import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

# Configuración básica del logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(APP_DIR, "app.log")),
        logging.StreamHandler(),
    ],
)

# Logger principal
logger = logging.getLogger(os.path.join(APP_DIR, "my_app"))

# Logger para errores críticos
critical_handler = logging.FileHandler(os.path.join(APP_DIR, "critical.log"))
critical_handler.setLevel(logging.CRITICAL)
critical_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
critical_handler.setFormatter(critical_formatter)
logger.addHandler(critical_handler)
