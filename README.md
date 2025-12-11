# bbb-led-webcontrol

Proyecto de referencia para controlar un LED desde Linux embebido a través de una pequeña aplicación web, con foco en:

- arquitectura limpia (domain / hal / app)
- testabilidad
- separación clara entre lógica de negocio, hardware y web
- entorno reproducible con Docker y CI

El objetivo no es el LED en sí, sino disponer de una base sólida para proyectos Linux embebidos controlables desde web.

---

## Objetivos

- Validar lógica de control **en host** (PC) antes de depender del hardware.
- Acceder a GPIO desde Linux de forma desacoplada mediante una HAL.
- Exponer el control vía HTTP y WebSocket, con una UI mínima.
- Mantener el proyecto ejecutable con:
  - `pytest`
  - `python -m app.web`
  - `docker build` + `docker run`
  - GitHub Actions (CI)

Este repositorio complementa al proyecto en C [`embedded-template`](https://github.com/angelsotob/embedded-template), aplicando ideas similares en un entorno Linux + Python.

---

## Arquitectura

Estructura en capas:

- `domain/`  
  Lógica de decisión pura.  
  No depende de Flask ni de hardware.

- `hal/`  
  Abstracción de acceso a GPIO.  
  Implementaciones fake y Linux (libgpiod).

- `app/`  
  Backend Flask + Socket.IO y orquestación.

- `tests/`  
  Tests unitarios de dominio, controlador y API HTTP.

Diagrama simplificado:

```
[ Web UI ] <-> [ Flask + Socket.IO ] <-> [ LedController ]
                                         |
                                         v
                                      [ Domain ]
                                         |
                                         v
                                   [ HAL (Fake / Linux) ]
                                         |
                                         v
                                      [ GPIO ]
```

---

## Ejecución local

```bash
git clone https://github.com/angelsotob/bbb-led-webcontrol.git
cd bbb-led-webcontrol

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

pytest
python -m app.web
```

Abrir en el navegador:

```
http://localhost:5000
```

---

## Ejecución con Docker

```bash
docker build -t bbb-led-webcontrol .
docker run --rm -p 5000:5000 bbb-led-webcontrol
```

Ejecutar tests en Docker:

```bash
docker run --rm bbb-led-webcontrol pytest
```

---

## Uso con GPIO real en Linux

La HAL real utiliza `libgpiod` y está preparada para BeagleBone u otras placas Linux.

Consultar `hal/gpio_linux.py` y ajustar permisos mediante reglas `udev`.

---

## Tests

Los tests cubren:

- Lógica de dominio
- Controlador de LED con HAL fake
- Endpoint HTTP `/led-state`

Se ejecutan con:

```bash
pytest
```

---

## Repositorios relacionados

- Firmware C con arquitectura limpia:  
  https://github.com/angelsotob/embedded-template
