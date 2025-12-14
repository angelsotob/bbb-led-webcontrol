from domain.logic import should_led_be_on


def test_led_on_when_sensor_above_threshold():
    assert should_led_be_on(3000) is True


def test_led_off_when_sensor_below_threshold():
    assert should_led_be_on(20) is False