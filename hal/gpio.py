from enum import Enum


class GpioState(Enum):
    LOW = 0
    HIGH = 1


class FakeGpio:
    """
    Implementación fake de GPIO.
    Útil para desarrollo y tests.
    """

    def __init__(self):
        self._pins = {}

    def set(self, pin: int, state: GpioState) -> None:
        self._pins[pin] = state

    def get(self, pin: int) -> GpioState:
        return self._pins.get(pin, GpioState.LOW)
