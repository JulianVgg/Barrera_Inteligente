from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# CONFIGURACIÓN DE ENTORNO
# ==============================

# En tu PC debe estar en False.
# En Raspberry Pi se cambiará a True.
HARDWARE_ENABLED = False

# En tu PC normalmente usamos cámara USB o webcam.
# En Raspberry Pi con cámara CSI se cambiará a True.
USE_PI_CAMERA = False

# ==============================
# RUTAS DEL PROYECTO
# ==============================

DB_PATH = BASE_DIR / "db" / "barrera.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"

CAPTURES_DIR = BASE_DIR / "captures"
AUTHORIZED_CAPTURES_DIR = CAPTURES_DIR / "authorized"
DENIED_CAPTURES_DIR = CAPTURES_DIR / "denied"
UNKNOWN_CAPTURES_DIR = CAPTURES_DIR / "unknown"

REPORTS_DIR = BASE_DIR / "reports" / "generated"

MODEL_PATH = BASE_DIR / "ai" / "models" / "vehicle_classifier.keras"

# ==============================
# CONFIGURACIÓN DE IA
# ==============================

IMAGE_SIZE = (128, 128)

# Confianza mínima para aceptar que sí hay vehículo
VEHICLE_CONFIDENCE_THRESHOLD = 0.70

# ==============================
# CONFIGURACIÓN DE PRESENCIA
# ==============================

# Distancia máxima para considerar que hay algo frente a la barrera
PRESENCE_DISTANCE_THRESHOLD_CM = 50

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================

APP_NAME = "Barrera Inteligente"
APP_VERSION = "1.0.0"