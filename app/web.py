import os
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO

from hal.gpio import FakeGpio
from app.led_controller import LedController
from app.control_loop import ControlLoop

# GPIO Linux (opcional en PC)
try:
    from hal.gpio_linux import LinuxGpio
except Exception:
    LinuxGpio = None  # En PC sin gpiod, seguimos con FakeGpio

# Sensor Linux ADC (opcional en PC)
try:
    from hal.sensor_linux_adc import LinuxAdcSensor
except Exception:
    LinuxAdcSensor = None

from hal.sensor_fake import FakeSensor

socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)
    socketio.init_app(app)

    # --- GPIO selection ---
    use_fake_gpio = os.getenv("USE_FAKE_GPIO", "1") == "1"
    if use_fake_gpio or LinuxGpio is None:
        gpio = FakeGpio()
        print("[GPIO] Using FakeGpio")
    else:
        chip_path = os.getenv("GPIO_CHIP", "/dev/gpiochip0")
        gpio = LinuxGpio(chip=chip_path)
        print(f"[GPIO] Using LinuxGpio on {chip_path}")

    led_line = int(os.getenv("LED_GPIO_LINE", "28"))  # BBB P9_12 -> line 28 on gpiochip0
    led = LedController(gpio=gpio, led_pin=led_line)

    # --- Sensor selection ---
    # En BBB: USE_FAKE_SENSOR=0 (y debe existir LinuxAdcSensor)
    use_fake_sensor = os.getenv("USE_FAKE_SENSOR", "1") == "1"
    if use_fake_sensor or LinuxAdcSensor is None:
        sensor = FakeSensor(initial_raw=0)
        print("[SENSOR] Using FakeSensor (host mode)")
    else:
        adc_channel = int(os.getenv("ADC_CHANNEL", "0"))           # AIN0
        iio_device = os.getenv("IIO_DEVICE", "iio:device0")
        sensor = LinuxAdcSensor(channel=adc_channel, iio_device=iio_device)
        print(f"[SENSOR] Using LinuxAdcSensor channel={adc_channel} device={iio_device}")

    # --- Control loop (sensor -> domain -> LED -> websocket status) ---
    period_s = float(os.getenv("CONTROL_PERIOD_S", "0.1"))

    def on_update(raw: int, led_on: bool):
        # Broadcast to all clients
        socketio.emit("status", {"sensor_raw": raw, "led_on": led_on})

    loop = ControlLoop(sensor=sensor, led=led, period_s=period_s, on_update=on_update)
    loop.start()

    # --- Routes ---
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(status="ok")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    # Si lo usas en systemd, evita el crash de Flask-SocketIO:
    allow_unsafe = os.getenv("ALLOW_UNSAFE_WERKZEUG", "1") == "1"
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=allow_unsafe)
