from enum import Enum, auto


class GpioState(Enum):
    LOW = 0
    HIGH = 1


class GpioInterface:
    """Interfaz abstracta para acceso a GPIO en Linux."""

    def set(self, pin: int, state: GpioState) -> None:
        raise NotImplementedError

    def get(self, pin: int) -> GpioState:
        raise NotImplementedError