# 🚦 bbb-led-webcontrol

Reference project for controlling an LED from embedded Linux through a
minimal web application.

The main goal is not the LED itself, but to provide a solid, testable
and reproducible base for Linux embedded projects that expose control
through a web interface.

Key focus areas:

-   Clean layered architecture (Domain / HAL / App)
-   Testability on host (no hardware required)
-   Clear separation between business logic, hardware access and web
    layer
-   Reproducible environment with Docker and CI
-   Real GPIO support for Linux boards (e.g., BeagleBone)

------------------------------------------------------------------------

# 🎯 Objectives

-   Validate control logic **on host (PC)** before depending on real
    hardware.
-   Access GPIO from Linux using a decoupled Hardware Abstraction Layer
    (HAL).
-   Expose LED control via HTTP and WebSocket.
-   Provide a minimal but functional web UI.
-   Keep the project executable using:
    -   `pytest`
    -   `python -m app.web`
    -   `docker build` + `docker run`
    -   GitHub Actions (CI-ready structure)

This repository complements the C firmware clean-architecture project:
https://github.com/angelsotob/embedded-template

------------------------------------------------------------------------

# 🏗 Architecture

The project follows a layered architecture inspired by clean
architecture principles.

Layers:

## 1️⃣ domain/

Pure business logic.

-   No dependency on Flask
-   No dependency on hardware
-   Fully unit-testable

Example: - `logic.py` → Decision rules for LED behavior

## 2️⃣ hal/

Hardware Abstraction Layer.

Provides interchangeable implementations:

-   `gpio_linux.py` → Real GPIO using libgpiod
-   `sensor_linux_adc.py` → Linux ADC implementation
-   `sensor_fake.py` → Fake sensor for testing
-   `gpio.py`, `sensor.py` → Abstraction interfaces

This allows running and testing the system without real hardware.

## 3️⃣ app/

Application layer.

-   Flask backend
-   Flask-SocketIO integration
-   Web routing
-   Control loop orchestration

Key modules:

-   `web.py` → Flask entry point
-   `led_controller.py` → Application-level coordination
-   `control_loop.py` → Periodic control execution
-   `templates/index.html` → Minimal web UI

## 4️⃣ tests/

Unit tests covering:

-   Domain logic
-   LED controller
-   Control loop
-   Sensor abstraction
-   HTTP endpoints
-   Web behavior

Tests are designed to run fully on host without GPIO access.

------------------------------------------------------------------------

# 🔄 Simplified Architecture Diagram

                 ┌─────────────┐
                 │   Web UI    │
                 └──────┬──────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Flask + Socket.IO  │
              └─────────┬──────────┘
                        │
                        ▼
                ┌───────────────┐
                │ LedController │
                └───────┬───────┘
                        │
                        ▼
                 ┌─────────────┐
                 │   Domain    │
                 │ (Pure Logic)│
                 └──────┬──────┘
                        │
                        ▼
           ┌─────────────────────────┐
           │ HAL (Fake / Linux GPIO) │
           └────────────┬────────────┘
                        │
                        ▼
                     ┌──────┐
                     │ GPIO │
                     └──────┘

Data flows from the Web UI down to the hardware layer.

Each layer depends only on the layer directly below it.
The Domain layer remains completely independent from Flask and GPIO.


------------------------------------------------------------------------


# ▶️ Local Execution

Clone the repository:

git clone https://github.com/angelsotob/bbb-led-webcontrol.git cd
bbb-led-webcontrol

* Create virtual environment:

    python -m venv .venv source .venv/bin/activate

* Install dependencies:

    pip install -r requirements.txt

* Run tests:

    pytest

* Start the web server:

    python -m app.web

* Open in browser:

    http://localhost:5000

------------------------------------------------------------------------

# 🐳 Running with Docker

* Build image:

    docker build -t bbb-led-webcontrol .

* Run container:

    docker run --rm -p 5000:5000 bbb-led-webcontrol

* Run tests inside Docker:

    docker run --rm bbb-led-webcontrol pytest

------------------------------------------------------------------------

# 🧪 Testing Strategy

The project is designed for hardware-independent testing.

Tests cover:

-   Domain decision logic
-   LED controller behavior with fake HAL
-   Control loop timing logic
-   HTTP endpoint `/led-state`
-   Web layer interactions

Run all tests with:

pytest

------------------------------------------------------------------------

# 🔌 Using Real GPIO on Linux

The Linux HAL uses `libgpiod` and is suitable for:

-   BeagleBone
-   Raspberry Pi (with adaptation)
-   Other embedded Linux boards

Refer to:

hal/gpio_linux.py

You may need to configure proper permissions using `udev` rules.

------------------------------------------------------------------------

# ⚙️ Running as a System Service

When executed as a `systemd` service (e.g., on BeagleBone), the project
may run using the Werkzeug development server with:

allow_unsafe_werkzeug=True

For production environments, consider using a proper WSGI server.

------------------------------------------------------------------------

# 📦 Project Structure

bbb-led-webcontrol/  
├── app/                 # Application layer (Flask + orchestration)  
│   ├── control_loop.py  
│   ├── led_controller.py  
│   ├── web.py  
│   └── templates/  
│       └── index.html  
│  
├── domain/              # Business logic (pure, hardware-independent)  
│   └── logic.py  
│  
├── hal/                 # Hardware abstraction layer  
│   ├── gpio.py  
│   ├── gpio_linux.py  
│   ├── sensor.py  
│   ├── sensor_linux_adc.py  
│   └── sensor_fake.py  
│
├── tests/               # Unit tests  
│   ├── test_logic.py  
│   ├── test_led_controller.py  
│   ├── test_control_loop.py  
│   ├── test_sensor.py  
│   └── test_web.py  
│  
├── vendor/              # Vendored dependencies  
├── Dockerfile  
├── requirements.txt  
└── README.md  

------------------------------------------------------------------------

# 🤝 Related Repositories

Clean architecture C firmware template:
https://github.com/angelsotob/embedded-template

------------------------------------------------------------------------

# 🤝 Contributing

1.  Fork the repository
2.  Create a branch: git checkout -b feature/new-feature
3.  Commit your changes: git commit -m "feat: add new feature"
4.  Push the branch: git push origin feature/new-feature
5.  Open a Pull Request

------------------------------------------------------------------------

# 📜 License

MIT License

------------------------------------------------------------------------

# 👨‍💻 Author

Angel Soto\
Embedded Systems Developer

