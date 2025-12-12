import gpiod
from gpiod.line import Direction, Value
import threading

from hal.gpio import GpioState


class LinuxGpio:
    """
    Implementación real de GPIO para Linux usando libgpiod v2.

    - chip: ruta del gpiochip (por defecto /dev/gpiochip0)
    - line_offset: número de línea dentro del chip (0..31)

    Mantiene las líneas pedidas mientras el proceso viva, para evitar
    parpadeos y errores de 'device busy'.
    """

    def __init__(self, chip: str = "/dev/gpiochip0"):
        self._chip_path = chip
        self._lock = threading.Lock()
        self._requests: dict[int, gpiod.LineRequest] = {}  # offset -> request

    def _ensure_line_requested(self, line_offset: int) -> gpiod.LineRequest:
        """
        Pide la línea si aún no está pedida y devuelve la request.
        """
        if line_offset in self._requests:
            return self._requests[line_offset]

        settings = gpiod.LineSettings(
            direction=Direction.OUTPUT,
            output_value=Value.INACTIVE,
        )

        # Pedimos la línea una vez y la guardamos
        request = gpiod.request_lines(
            self._chip_path,
            consumer="bbb-webcontrol",
            config={line_offset: settings},
        )

        self._requests[line_offset] = request
        return request

    def set(self, line_offset: int, state: GpioState) -> None:
        """
        Establece el valor de un GPIO como HIGH o LOW.

        line_offset: número de línea dentro del chip (0..31)
        state: GpioState.HIGH o GpioState.LOW
        """
        value = Value.ACTIVE if state == GpioState.HIGH else Value.INACTIVE

        with self._lock:
            try:
                request = self._ensure_line_requested(line_offset)
                request.set_value(line_offset, value)
            except OSError as e:
                print(f"[GPIO] Error setting line {line_offset}: {e}")
