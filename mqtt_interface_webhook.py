
import os
import json
import logging
import pytz
from datetime import datetime
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC_JSON = "meshtastic/+/json/+/+"
TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
WATCH_CHANNELS = os.getenv("WATCH_CHANNELS", "")

if WATCH_CHANNELS:
    WATCH_CHANNELS = [int(c.strip()) for c in WATCH_CHANNELS.split(",")]
else:
    WATCH_CHANNELS = []

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

client = mqtt.Client()

def register_mqtt_listener(notify_func):
    def on_connect(client, userdata, flags, rc):
        logging.info("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC_JSON)

    def on_mqtt_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            logging.debug(f"MQTT received on {msg.topic}: {payload}")

            sender = payload.get("sender", "unknown")
            text = payload.get("payload", {}).get("text", None)
            channel = payload.get("channel", "?")
            timestamp = payload.get("timestamp", None)

            if text:
                if WATCH_CHANNELS and channel not in WATCH_CHANNELS:
                    logging.debug(f"Ignoring message on channel {channel} (not in WATCH_CHANNELS)")
                    return

                time_str = ""
                if timestamp:
                    try:
                        tz = pytz.timezone(TIMEZONE)
                        time_str = datetime.fromtimestamp(timestamp, tz).strftime(" @ %I:%M %p %Z")
                    except Exception:
                        time_str = ""

                message = f"📡 [{channel}] {sender}{time_str}: {text}"
                logging.info(f"Forwarding to Discord Webhook: {message}")
                notify_func(message)

        except UnicodeDecodeError as e:
            logging.error(f"Encoding error: {e}")
        except Exception as e:
            logging.error(f"Error handling MQTT message: {e}")

    client.on_connect = on_connect
    client.message_callback_add(MQTT_TOPIC_JSON, on_mqtt_message)
    client.connect_async(MQTT_BROKER, MQTT_PORT)
    client.loop_start()
