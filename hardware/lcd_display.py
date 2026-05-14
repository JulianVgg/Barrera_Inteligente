from utils.config import HARDWARE_ENABLED


class LCDDisplay:
    """
    Control del LCD I2C.

    En PC:
        Simula mensajes en consola.

    En Raspberry:
        Se puede conectar a un LCD real I2C.
    """

    def __init__(self):
        self.enabled = HARDWARE_ENABLED

        if self.enabled:
            try:
                import smbus2  # noqa: F401
                print("LCD I2C listo para inicializar.")
            except Exception as error:
                print(f"No se pudo inicializar LCD I2C: {error}")
                print("El sistema continuará en modo simulado.")
                self.enabled = False

    def show_message(self, line1, line2=""):
        if not self.enabled:
            print("[MODO SIMULADO LCD]")
            print(f"> {line1}")

            if line2:
                print(f"> {line2}")

            return

        # Aquí se implementará el envío real al LCD en Raspberry.
        print("[LCD REAL]")
        print(f"> {line1}")

        if line2:
            print(f"> {line2}")

    def clear(self):
        if not self.enabled:
            print("[MODO SIMULADO LCD] Pantalla limpiada.")
            return

        print("[LCD REAL] Pantalla limpiada.")