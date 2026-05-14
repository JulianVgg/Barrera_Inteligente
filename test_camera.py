import cv2
from datetime import datetime

from camera.camera_service import CameraService
from utils.config import UNKNOWN_CAPTURES_DIR


def save_capture(frame):
    UNKNOWN_CAPTURES_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = UNKNOWN_CAPTURES_DIR / f"capture_{timestamp}.jpg"

    cv2.imwrite(str(image_path), frame)

    print(f"Imagen guardada en: {image_path}")


def main():
    camera = CameraService(camera_index=0)

    try:
        camera.start()

        print("Cámara iniciada.")
        print("Controles:")
        print("  q = salir")
        print("  c = capturar imagen")

        while True:
            ret, frame = camera.read_frame()

            if not ret:
                print("No se pudo leer frame de la cámara.")
                break

            cv2.imshow("Prueba de Cámara - Barrera Inteligente", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("c"):
                save_capture(frame)

            if key == ord("q"):
                break

    except Exception as error:
        print(f"Error en cámara: {error}")

    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()