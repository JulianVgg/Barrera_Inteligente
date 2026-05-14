from utils.config import (
    APP_NAME,
    APP_VERSION,
    BASE_DIR,
    HARDWARE_ENABLED,
    USE_PI_CAMERA,
    DB_PATH,
    MODEL_PATH,
)

from db.database import (
    init_db,
    list_authorized_plates,
    list_recent_logs,
)


def show_startup_info():
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


def show_authorized_plates():
    plates = list_authorized_plates()

    print("\n========== PLACAS AUTORIZADAS ==========")

    if not plates:
        print("No hay placas autorizadas registradas.")
        return

    for plate in plates:
        print(
            f"ID: {plate['id']} | "
            f"Placa: {plate['plate_number']} | "
            f"Propietario: {plate['owner_name']} | "
            f"Tipo: {plate['vehicle_type']} | "
            f"Estado: {plate['status']}"
        )


def show_recent_logs():
    logs = list_recent_logs(limit=10)

    print("\n========== ÚLTIMOS REGISTROS ==========")

    if not logs:
        print("No hay registros de acceso todavía.")
        return

    for log in logs:
        print(
            f"ID: {log['id']} | "
            f"Fecha: {log['event_date']} | "
            f"Hora: {log['event_time']} | "
            f"Placa: {log['plate_detected']} | "
            f"Estado: {log['access_status']} | "
            f"Motivo: {log['reason']}"
        )


def main():
    show_startup_info()

    print("Inicializando base de datos...")
    init_db()
    print("Base de datos lista.")

    show_authorized_plates()
    show_recent_logs()

    print("\nProyecto iniciado correctamente.")


if __name__ == "__main__":
    main()