import cv2

from camera.camera_service import CameraService
from db.database import init_db
from hardware.barrier_servo import BarrierServo
from hardware.distance_sensor import PresenceSensor
from hardware.lcd_display import LCDDisplay
from services.access_control import validate_access


def main():
    init_db()

    camera = CameraService(camera_index=0)
    barrier = BarrierServo()
    sensor = PresenceSensor()
    lcd = LCDDisplay()

    try:
        camera.start()

        print("===================================")
        print("  PRUEBA DE FLUJO DE ACCESO")
        print("===================================")
        print("Controles:")
        print("  v = validar acceso")
        print("  q = salir")
        print("-----------------------------------")

        lcd.show_message("Sistema listo", "Esperando vehiculo")

        while True:
            ret, frame = camera.read_frame()

            if not ret:
                print("No se pudo leer frame de la cámara.")
                break

            cv2.imshow("Flujo de Acceso - Barrera Inteligente", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("v"):
                present, distance = sensor.is_present()

                if not present:
                    print("No hay presencia física frente a la barrera.")
                    lcd.show_message("Sin vehiculo", "Acceso bloqueado")
                    barrier.denied_signal()
                    continue

                print(f"Presencia detectada a {distance} cm.")
                lcd.show_message("Vehiculo cerca", f"{distance} cm")

                plate = input("Ingrese la placa a validar: ")

                result = validate_access(
                    plate_number=plate,
                    frame=frame,
                    vehicle_confidence=None,
                    distance_cm=distance,
                )

                print("-----------------------------------")
                print(result["message"])
                print(f"Estado: {result['status']}")
                print(f"Registro ID: {result['log_id']}")

                if result.get("image_path"):
                    print(f"Imagen guardada: {result['image_path']}")

                print("-----------------------------------")

                if result["authorized"]:
                    lcd.show_message("Acceso", "Autorizado")
                    barrier.open()
                else:
                    lcd.show_message("Acceso", "Denegado")
                    barrier.denied_signal()

            if key == ord("q"):
                break

    except Exception as error:
        print(f"Error en flujo de acceso: {error}")

    finally:
        camera.stop()
        barrier.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()