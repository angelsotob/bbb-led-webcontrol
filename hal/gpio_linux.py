import gpiod
from gpiod.line import Direction, Value

from hal.gpio import GpioState


class LinuxGpio:
    """
    Implementación real de GPIO para Linux usando libgpiod v2.

    Pensado para BeagleBone Black:
    - chip: /dev/gpiochip0
    - line_offset: número de línea dentro del chip (0..31)
    """

    def __init__(self, chip: str = "/dev/gpiochip0"):
        self._chip_path = chip

    def set(self, line_offset: int, state: GpioState) -> None:
        """
        Establece el valor de un GPIO como HIGH o LOW.

        line_offset: número de línea dentro del chip (0..31)
        state: GpioState.HIGH o GpioState.LOW
        """
        value = Value.ACTIVE if state == GpioState.HIGH else Value.INACTIVE

        settings = gpiod.LineSettings(
            direction=Direction.OUTPUT,
            output_value=value,
        )

        # Petición corta por simplicidad: abre, fija valor, cierra.
        # Más adelante se puede optimizar dejando la petición viva.
        with gpiod.request_lines(
            self._chip_path,
            consumer="bbb-webcontrol",
            config={line_offset: settings},
        ) as request:
            request.set_value(line_offset, value)
