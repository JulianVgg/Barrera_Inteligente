import sqlite3
from datetime import datetime
from pathlib import Path

from utils.config import DB_PATH, SCHEMA_PATH


def get_connection():
    """
    Crea y retorna una conexión a la base de datos SQLite.
    row_factory permite acceder a los campos por nombre.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Inicializa la base de datos usando el archivo schema.sql.
    Crea las tablas si todavía no existen.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            conn.executescript(file.read())
        conn.commit()


def normalize_plate(plate_number):
    """
    Limpia y normaliza una placa:
    - Convierte a mayúsculas
    - Quita espacios
    - Quita guiones
    """
    if plate_number is None:
        return None

    return (
        plate_number
        .upper()
        .replace(" ", "")
        .replace("-", "")
        .strip()
    )


def add_authorized_plate(plate_number, owner_name, vehicle_type="Automovil"):
    """
    Agrega una placa autorizada a la base de datos.
    """
    plate_number = normalize_plate(plate_number)

    if not plate_number:
        raise ValueError("La placa no puede estar vacía.")

    if not owner_name or not owner_name.strip():
        raise ValueError("El nombre del propietario no puede estar vacío.")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO authorized_plates 
            (plate_number, owner_name, vehicle_type, status)
            VALUES (?, ?, ?, 'ACTIVE')
            """,
            (plate_number, owner_name.strip(), vehicle_type.strip()),
        )
        conn.commit()
        return cursor.lastrowid


def get_authorized_plate(plate_number):
    """
    Busca una placa activa en la base de datos.
    Retorna la placa si existe, de lo contrario retorna None.
    """
    plate_number = normalize_plate(plate_number)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM authorized_plates
            WHERE plate_number = ?
            AND status = 'ACTIVE'
            """,
            (plate_number,),
        )
        return cursor.fetchone()


def list_authorized_plates():
    """
    Lista todas las placas autorizadas.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM authorized_plates
            ORDER BY created_at DESC
            """
        )
        return cursor.fetchall()


def deactivate_authorized_plate(plate_number):
    """
    Desactiva una placa sin borrarla físicamente.
    """
    plate_number = normalize_plate(plate_number)
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE authorized_plates
            SET status = 'INACTIVE',
                updated_at = ?
            WHERE plate_number = ?
            """,
            (updated_at, plate_number),
        )
        conn.commit()
        return cursor.rowcount


def register_access_log(
    plate_detected,
    access_status,
    reason,
    vehicle_confidence=None,
    distance_cm=None,
    image_path=None,
):
    """
    Registra un evento de acceso.

    access_status puede ser:
    - AUTORIZADO
    - NO_AUTORIZADO
    - SIN_VEHICULO
    - PLACA_NO_RECONOCIDA
    """
    now = datetime.now()
    event_date = now.strftime("%Y-%m-%d")
    event_time = now.strftime("%H:%M:%S")

    plate_detected = normalize_plate(plate_detected) if plate_detected else None

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO access_logs
            (
                plate_detected,
                event_date,
                event_time,
                access_status,
                reason,
                vehicle_confidence,
                distance_cm,
                image_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                plate_detected,
                event_date,
                event_time,
                access_status,
                reason,
                vehicle_confidence,
                distance_cm,
                str(image_path) if image_path else None,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_logs_by_date_range(start_date, end_date):
    """
    Obtiene registros de acceso por rango de fechas.

    Formato esperado:
    YYYY-MM-DD
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM access_logs
            WHERE event_date BETWEEN ? AND ?
            ORDER BY event_date DESC, event_time DESC
            """,
            (start_date, end_date),
        )
        return cursor.fetchall()


def list_recent_logs(limit=20):
    """
    Lista los últimos registros de acceso.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM access_logs
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()


def register_system_event(event_type, description):
    """
    Registra eventos internos del sistema.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO system_events
            (event_type, description)
            VALUES (?, ?)
            """,
            (event_type, description),
        )
        conn.commit()
        return cursor.lastrowid


def seed_test_data():
    """
    Inserta datos de prueba para comenzar.
    Si la placa ya existe, no rompe el programa.
    """
    test_plates = [
        ("P123ABC", "Vehículo de prueba 1", "Automovil"),
        ("P456DEF", "Vehículo de prueba 2", "Pickup"),
        ("M789GHI", "Moto de prueba", "Motocicleta"),
    ]

    for plate, owner, vehicle_type in test_plates:
        try:
            add_authorized_plate(plate, owner, vehicle_type)
            print(f"Placa agregada: {plate}")
        except sqlite3.IntegrityError:
            print(f"La placa ya existe: {plate}")

    register_access_log(
        plate_detected="P123ABC",
        access_status="AUTORIZADO",
        reason="Registro de prueba autorizado",
        vehicle_confidence=0.95,
        distance_cm=35.5,
    )

    register_access_log(
        plate_detected="X999XYZ",
        access_status="NO_AUTORIZADO",
        reason="Registro de prueba no autorizado",
        vehicle_confidence=0.91,
        distance_cm=40.2,
    )

    register_system_event(
        event_type="INIT",
        description="Base de datos inicializada con datos de prueba",
    )


def print_database_summary():
    """
    Imprime un resumen simple para verificar que todo funciona.
    """
    print("\n========== PLACAS AUTORIZADAS ==========")
    plates = list_authorized_plates()

    for plate in plates:
        print(
            f"ID: {plate['id']} | "
            f"Placa: {plate['plate_number']} | "
            f"Propietario: {plate['owner_name']} | "
            f"Tipo: {plate['vehicle_type']} | "
            f"Estado: {plate['status']}"
        )

    print("\n========== REGISTROS RECIENTES ==========")
    logs = list_recent_logs()

    for log in logs:
        print(
            f"ID: {log['id']} | "
            f"Fecha: {log['event_date']} | "
            f"Hora: {log['event_time']} | "
            f"Placa: {log['plate_detected']} | "
            f"Estado: {log['access_status']} | "
            f"Motivo: {log['reason']}"
        )


if __name__ == "__main__":
    print("Inicializando base de datos...")
    init_db()

    print("Insertando datos de prueba...")
    seed_test_data()

    print_database_summary()

    print("\nBase de datos lista correctamente.")