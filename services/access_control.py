from datetime import datetime
import cv2

from db.database import (
    get_authorized_plate,
    register_access_log,
)

from utils.config import (
    AUTHORIZED_CAPTURES_DIR,
    DENIED_CAPTURES_DIR,
    UNKNOWN_CAPTURES_DIR,
)


def save_event_image(frame, folder, prefix):
    """
    Guarda una imagen relacionada a un evento de acceso.
    """
    folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = folder / f"{prefix}_{timestamp}.jpg"

    cv2.imwrite(str(image_path), frame)

    return image_path


def validate_access(
    plate_number,
    frame=None,
    vehicle_confidence=None,
    distance_cm=None,
):
    """
    Valida si una placa tiene autorización de acceso.

    Por ahora la placa se ingresa manualmente.
    Luego esta función recibirá la placa desde OCR o reconocimiento.
    """

    if not plate_number or not plate_number.strip():
        image_path = None

        if frame is not None:
            image_path = save_event_image(
                frame=frame,
                folder=UNKNOWN_CAPTURES_DIR,
                prefix="unknown_plate",
            )

        log_id = register_access_log(
            plate_detected=None,
            access_status="PLACA_NO_RECONOCIDA",
            reason="No se ingresó o reconoció una placa válida",
            vehicle_confidence=vehicle_confidence,
            distance_cm=distance_cm,
            image_path=image_path,
        )

        return {
            "authorized": False,
            "status": "PLACA_NO_RECONOCIDA",
            "message": "No se ingresó una placa válida.",
            "log_id": log_id,
            "image_path": image_path,
        }

    plate_number = plate_number.upper().replace(" ", "").replace("-", "").strip()

    authorized_plate = get_authorized_plate(plate_number)

    if authorized_plate:
        image_path = None

        if frame is not None:
            image_path = save_event_image(
                frame=frame,
                folder=AUTHORIZED_CAPTURES_DIR,
                prefix=f"authorized_{plate_number}",
            )

        log_id = register_access_log(
            plate_detected=plate_number,
            access_status="AUTORIZADO",
            reason="Placa autorizada registrada en base de datos",
            vehicle_confidence=vehicle_confidence,
            distance_cm=distance_cm,
            image_path=image_path,
        )

        return {
            "authorized": True,
            "status": "AUTORIZADO",
            "message": f"Acceso autorizado para placa {plate_number}.",
            "plate": dict(authorized_plate),
            "log_id": log_id,
            "image_path": image_path,
        }

    image_path = None

    if frame is not None:
        image_path = save_event_image(
            frame=frame,
            folder=DENIED_CAPTURES_DIR,
            prefix=f"denied_{plate_number}",
        )

    log_id = register_access_log(
        plate_detected=plate_number,
        access_status="NO_AUTORIZADO",
        reason="Placa no encontrada en la base de datos",
        vehicle_confidence=vehicle_confidence,
        distance_cm=distance_cm,
        image_path=image_path,
    )

    return {
        "authorized": False,
        "status": "NO_AUTORIZADO",
        "message": f"Acceso denegado para placa {plate_number}.",
        "log_id": log_id,
        "image_path": image_path,
    }