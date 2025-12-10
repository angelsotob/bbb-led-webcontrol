# Imagen base ligera de Python
FROM python:3.12-slim

# No generar .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Salida de logs sin buffer
ENV PYTHONUNBUFFERED=1

# Crear directorio de la app
WORKDIR /app

# Instalar dependencias del sistema si hiciera falta (libgpiod, etc.)
# De momento solo dejamos la estructura lista:
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY app/ app/
COPY domain/ domain/
COPY hal/ hal/
COPY tests/ tests/

# Puerto para la aplicación web
EXPOSE 5000

# Comando por defecto: lanzar la app
CMD ["python", "-m", "app.web"]
