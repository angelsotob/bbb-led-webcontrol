from hal.sensor import Sensor, SensorReading


class LinuxAdcSensor(Sensor):
    """
    Reads BBB ADC via sysfs IIO.
    Example path: /sys/bus/iio/devices/iio:device0/in_voltage0_raw
    """

    def __init__(self, channel: int = 0, iio_device: str = "iio:device0"):
        self._path = f"/sys/bus/iio/devices/{iio_device}/in_voltage{channel}_raw"

    def read(self) -> SensorReading:
        with open(self._path, "r", encoding="utf-8") as f:
            raw = int(f.read().strip())
        return SensorReading(raw=raw)
