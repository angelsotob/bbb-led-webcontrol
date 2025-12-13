import threading
import time
from typing import Callable

from hal.sensor import Sensor
from app.led_controller import LedController


class ControlLoop:
    def __init__(
        self,
        sensor: Sensor,
        led: LedController,
        period_s: float = 0.1,
        on_update: Callable[[int, bool], None] | None = None,
    ):
        self._sensor = sensor
        self._led = led
        self._period_s = period_s
        self._on_update = on_update
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1)

    def _run(self) -> None:
        while not self._stop.is_set():
            reading = self._sensor.read()
            led_on = self._led.update(reading.raw)

            if self._on_update:
                self._on_update(reading.raw, led_on)

            time.sleep(self._period_s)
