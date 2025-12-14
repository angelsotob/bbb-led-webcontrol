from domain.logic import should_led_be_on
from hal.gpio import GpioState

class LedController:
    def __init__(self, gpio, led_pin: int):
        self._gpio = gpio
        self._led_pin = led_pin

    def update(self, sensor_value: int) -> bool:
        led_on = should_led_be_on(sensor_value)

        state = GpioState.HIGH if led_on else GpioState.LOW
        self._gpio.set(self._led_pin, state)

        return led_on