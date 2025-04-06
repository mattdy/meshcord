# Dockerfile for Mesh Watchdog (Webhook Edition)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot_webhook.py mqtt_interface_webhook.py ./
COPY .env .

CMD ["python", "bot_webhook.py"]