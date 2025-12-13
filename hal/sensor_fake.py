from hal.sensor import Sensor, SensorReading


class FakeSensor(Sensor):
    def __init__(self, initial_raw: int = 0):
        self._raw = initial_raw

    def set_raw(self, raw: int) -> None:
        self._raw = int(raw)

    def read(self) -> SensorReading:
        return SensorReading(raw=self._raw)
