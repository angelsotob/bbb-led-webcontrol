import time
from hal.sensor_fake import FakeSensor
from hal.gpio import FakeGpio
from app.led_controller import LedController
from app.control_loop import ControlLoop


def test_control_loop_emits_updates():
    sensor = FakeSensor(initial_raw=0)
    gpio = FakeGpio()
    led = LedController(gpio=gpio, led_pin=17)

    updates = []

    def on_update(raw, led_on):
        updates.append((raw, led_on))

    loop = ControlLoop(sensor=sensor, led=led, period_s=0.01, on_update=on_update)
    loop.start()

    sensor.set_raw(10)
    time.sleep(0.03)

    sensor.set_raw(90)
    time.sleep(0.03)

    loop.stop()

    assert len(updates) > 0
    assert any(raw == 10 for raw, _ in updates)
    assert any(raw == 90 for raw, _ in updates)
