from hal.sensor_fake import FakeSensor


def test_fake_sensor_returns_current_raw_value():
    s = FakeSensor(initial_raw=123)
    assert s.read().raw == 123

    s.set_raw(456)
    assert s.read().raw == 456
