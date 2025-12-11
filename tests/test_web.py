import json

from app.web import create_app


def _create_test_client():
    app = create_app()
    app.config.update({"TESTING": True})
    return app.test_client()


def test_led_state_on_when_sensor_above_threshold():
    client = _create_test_client()

    response = client.get("/led-state?sensor_value=80")

    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert data["sensor_value"] == 80
    assert data["led_on"] is True


def test_led_state_off_when_sensor_below_threshold():
    client = _create_test_client()

    response = client.get("/led-state?sensor_value=20")

    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert data["sensor_value"] == 20
    assert data["led_on"] is False


def test_led_state_requires_sensor_value():
    client = _create_test_client()

    response = client.get("/led-state")

    assert response.status_code == 400
    data = json.loads(response.data.decode("utf-8"))
    assert "error" in data
