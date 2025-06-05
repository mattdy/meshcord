import os
import logging
import time
from dotenv import load_dotenv
from mqtt_interface_webhook import setup_mqtt

load_dotenv()

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s - %(levelname)s - %(message)s")

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
TIMEZONE = os.getenv("TIMEZONE", "UTC")
WATCH_CHANNELS = [int(ch) for ch in os.getenv("WATCH_CHANNELS", "").split(",") if ch.strip().isdigit()]

if not DISCORD_WEBHOOK_URL:
    logging.error("DISCORD_WEBHOOK_URL not set in .env file.")
    exit(1)

logging.info("Meshcord starting...")
logging.info(f"Logging: {LOGLEVEL}")
logging.info(f"Webhook: {DISCORD_WEBHOOK_URL}")
logging.info(f"MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
logging.info(f"Timezone: {TIMEZONE}")
logging.info(f"Watching channels: {WATCH_CHANNELS if WATCH_CHANNELS else 'All'}")

setup_mqtt(
    webhook_url=DISCORD_WEBHOOK_URL,
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    timezone=TIMEZONE,
    watch_channels=WATCH_CHANNELS
)

# Keep the container alive
while True:
    time.sleep(60)
