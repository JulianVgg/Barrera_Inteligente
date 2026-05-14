from utils.config import HARDWARE_ENABLED, PRESENCE_DISTANCE_THRESHOLD_CM


class PresenceSensor:
    """
    Controla el sensor ultrasónico HC-SR04.

    En PC:
        Simula una distancia.

    En Raspberry:
        Lee distancia real con GPIO.
    """

    def __init__(self):
        self.enabled = HARDWARE_ENABLED
        self.threshold_cm = PRESENCE_DISTANCE_THRESHOLD_CM
        self.sensor = None

        if self.enabled:
            try:
                from gpiozero import DistanceSensor
                from hardware.pins import ULTRASONIC_TRIGGER_PIN, ULTRASONIC_ECHO_PIN

                self.sensor = DistanceSensor(
                    echo=ULTRASONIC_ECHO_PIN,
                    trigger=ULTRASONIC_TRIGGER_PIN,
                    max_distance=2
                )

                print("Sensor ultrasónico inicializado correctamente.")

            except Exception as error:
                print(f"No se pudo inicializar el sensor ultrasónico: {error}")
                print("El sistema continuará en modo simulado.")
                self.enabled = False

    def get_distance_cm(self):
        if not self.enabled:
            simulated_distance = 30.0
            print(f"[MODO SIMULADO] Distancia detectada: {simulated_distance} cm")
            return simulated_distance

        distance_m = self.sensor.distance
        return round(distance_m * 100, 2)

    def is_present(self):
        distance = self.get_distance_cm()
        present = distance <= self.threshold_cm

        return present, distance