from utils.config import (
    APP_NAME,
    APP_VERSION,
    BASE_DIR,
    HARDWARE_ENABLED,
    USE_PI_CAMERA,
    DB_PATH,
    MODEL_PATH,
)


def main():
    print("===================================")
    print(f"  {APP_NAME.upper()} - INICIO")
    print("===================================")
    print(f"Versión: {APP_VERSION}")
    print(f"Ruta del proyecto: {BASE_DIR}")
    print(f"Base de datos: {DB_PATH}")
    print(f"Modelo IA: {MODEL_PATH}")
    print("-----------------------------------")
    print(f"Hardware habilitado: {HARDWARE_ENABLED}")
    print(f"Usar cámara Raspberry: {USE_PI_CAMERA}")
    print("-----------------------------------")
    print("Proyecto iniciado correctamente.")


if __name__ == "__main__":
    main()