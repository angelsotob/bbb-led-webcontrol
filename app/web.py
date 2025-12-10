from flask import Flask, jsonify, request
from domain.logic import should_led_be_on


def create_app():
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(status="ok")

    @app.route("/led-state", methods=["GET"])
    def led_state():
        # Leer el parámetro sensor_value de la query string
        raw_value = request.args.get("sensor_value", type=int)

        if raw_value is None:
            return jsonify(error="sensor_value query parameter is required"), 400

        led_on = should_led_be_on(raw_value)

        return jsonify(
            sensor_value=raw_value,
            led_on=led_on,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
