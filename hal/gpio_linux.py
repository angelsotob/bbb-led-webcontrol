# hal/gpio_linux.py
import gpiod
from hal.gpio import GpioState


class LinuxGpio:
    """
    Implementación real de GPIO para Linux usando libgpiod.
    """

    def __init__(self, chip_name: str = "gpiochip0"):
        self._chip = gpiod.Chip(chip_name)

    def set(self, line_offset: int, state: GpioState) -> None:
        line = self._chip.get_line(line_offset)
        line.request(
            consumer="bbb-led-webcontrol",
            type=gpiod.LINE_REQ_DIR_OUT,
        )
        line.set_value(1 if state == GpioState.HIGH else 0)
        line.release()

    def get(self, line_offset: int) -> GpioState:
        line = self._chip.get_line(line_offset)
        line.request(
            consumer="bbb-led-webcontrol",
            type=gpiod.LINE_REQ_DIR_IN,
        )
        value = line.get_value()
        line.release()

        return GpioState.HIGH if value else GpioState.LOW
