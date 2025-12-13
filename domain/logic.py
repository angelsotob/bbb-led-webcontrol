LED_THRESHOLD = 2050


def should_led_be_on(sensor_value: int) -> bool:
    """Decide si el LED debe estar encendido en función del valor del sensor."""
    return sensor_value >= LED_THRESHOLD