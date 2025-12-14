from app.led_controller import LedController
from hal.gpio import FakeGpio, GpioState


def test_led_controller_turns_on_led():
    gpio = FakeGpio()
    led = LedController(gpio=gpio, led_pin=1)

    result = led.update(3000)

    assert result is True
    assert gpio.get(1) == GpioState.HIGH


def test_led_controller_turns_off_led():
    gpio = FakeGpio()
    led = LedController(gpio=gpio, led_pin=1)

    result = led.update(10)

    assert result is False
    assert gpio.get(1) == GpioState.LOW
