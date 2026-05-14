from time import sleep

from utils.config import HARDWARE_ENABLED


class BarrierServo:
    """
    Controla la talanquera.

    En PC:
        HARDWARE_ENABLED = False
        Solo simula abrir/cerrar.

    En Raspberry:
        HARDWARE_ENABLED = True
        Usará GPIO para mover el servo.
    """

    def __init__(self):
        self.enabled = HARDWARE_ENABLED
        self.servo = None

        if self.enabled:
            try:
                from gpiozero import Servo
                from hardware.pins import SERVO_PIN

                self.servo = Servo(SERVO_PIN)
                print("Servo inicializado correctamente.")
            except Exception as error:
                print(f"No se pudo inicializar el servo: {error}")
                print("El sistema continuará en modo simulado.")
                self.enabled = False

    def open(self):
        if not self.enabled:
            print("[MODO SIMULADO] Barrera abierta.")
            sleep(2)
            self.close()
            return

        print("Abriendo barrera...")
        self.servo.max()
        sleep(3)
        self.close()

    def close(self):
        if not self.enabled:
            print("[MODO SIMULADO] Barrera cerrada.")
            return

        print("Cerrando barrera...")
        self.servo.min()
        sleep(0.5)

    def denied_signal(self):
        if not self.enabled:
            print("[MODO SIMULADO] Acceso denegado. Barrera permanece cerrada.")
            return

        print("Acceso denegado. Barrera permanece cerrada.")

    def stop(self):
        if self.servo:
            self.servo.detach()