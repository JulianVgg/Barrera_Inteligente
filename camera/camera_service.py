import cv2

from utils.config import USE_PI_CAMERA


class CameraService:
    """
    Servicio de cámara.

    En PC:
        USE_PI_CAMERA = False
        Usa webcam o cámara USB con OpenCV.

    En Raspberry Pi:
        USE_PI_CAMERA = True
        Usará Picamera2 para cámara CSI.
    """

    def __init__(self, camera_index=0):
        self.use_pi_camera = USE_PI_CAMERA
        self.camera_index = camera_index
        self.cap = None
        self.picam2 = None

    def start(self):
        if self.use_pi_camera:
            self._start_pi_camera()
        else:
            self._start_usb_camera()

    def _start_usb_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise RuntimeError(
                "No se pudo abrir la cámara. "
                "Prueba cambiando camera_index de 0 a 1."
            )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("Cámara USB/Webcam iniciada correctamente.")

    def _start_pi_camera(self):
        try:
            from picamera2 import Picamera2

            self.picam2 = Picamera2()
            config = self.picam2.create_preview_configuration(
                main={
                    "size": (640, 480),
                    "format": "RGB888",
                }
            )
            self.picam2.configure(config)
            self.picam2.start()

            print("Cámara Raspberry Pi iniciada correctamente.")

        except Exception as error:
            raise RuntimeError(f"No se pudo iniciar la cámara Raspberry Pi: {error}")

    def read_frame(self):
        if self.use_pi_camera:
            return self._read_pi_frame()

        return self._read_usb_frame()

    def _read_usb_frame(self):
        if self.cap is None:
            return False, None

        return self.cap.read()

    def _read_pi_frame(self):
        if self.picam2 is None:
            return False, None

        frame = self.picam2.capture_array()

        # Picamera2 entrega RGB, OpenCV usa BGR.
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return True, frame

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        if self.picam2 is not None:
            self.picam2.stop()
            self.picam2 = None

        print("Cámara detenida correctamente.")