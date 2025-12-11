import os
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit

from hal.gpio import FakeGpio
from app.led_controller import LedController

try:
    from hal.gpio_linux import LinuxGpio
except Exception:
    LinuxGpio = None  # En PC sin gpiod, seguimos con FakeGpio

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    socketio.init_app(app)

    use_fake = os.getenv("USE_FAKE_GPIO", "1") == "1"

    if use_fake or LinuxGpio is None:
        gpio = FakeGpio()
        print("[GPIO] Using FakeGpio")
    else:
        gpio = LinuxGpio(chip="/dev/gpiochip0")
        print("[GPIO] Using LinuxGpio on /dev/gpiochip0")

    # En PC da igual; en BBB usaremos 28 (P9_12)
    LED_GPIO_LINE = int(os.getenv("LED_GPIO_LINE", "28"))

    led = LedController(gpio=gpio, led_pin=LED_GPIO_LINE)

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

    @socketio.on("sensor_update")
    def handle_sensor_update(data):
        sensor_value = data.get("sensor_value")

        if sensor_value is None:
            emit("error", {"error": "sensor_value missing"})
            return

        led_on = led.update(sensor_value)

        emit("led_state", {
            "sensor_value": sensor_value,
            "led_on": led_on
        })

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000)
