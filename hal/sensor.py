from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SensorReading:
    raw: int


class Sensor(Protocol):
    def read(self) -> SensorReading:
        """Return a sensor reading (raw ADC units)."""
        ...
