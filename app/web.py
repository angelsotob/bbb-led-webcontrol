from flask import Flask, jsonify, request
from hal.gpio import FakeGpio
#from hal.gpio_linux import LinuxGpio
from app.led_controller import LedController


def create_app(use_fake_gpio: bool = True):
    app = Flask(__name__)

    if use_fake_gpio:
        gpio = FakeGpio()
    else:
        from hal.gpio_linux import LinuxGpio
        gpio = LinuxGpio()

    LED_GPIO_PIN = 17
    led = LedController(gpio=gpio, led_pin=LED_GPIO_PIN)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(status="ok")

    @app.route("/led-state", methods=["GET"])
    def led_state():
        raw_value = request.args.get("sensor_value", type=int)
        if raw_value is None:
            return jsonify(error="sensor_value query parameter is required"), 400

        led_on = led.update(raw_value)

        return jsonify(
            sensor_value=raw_value,
            led_on=led_on,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
