import json
import pytz
import logging
import requests
from datetime import datetime
import paho.mqtt.client as mqtt

client = mqtt.Client()

def setup_mqtt(webhook_url, broker, port, timezone, watch_channels):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected to MQTT broker at {broker}:{port}")
            client.subscribe("meshtastic/2/json/#")
            logging.info("Subscribed to topic: meshtastic/2/json/#")
        else:
            logging.error(f"MQTT connection failed with code {rc}")

    def on_message(client, userdata, msg):
        logging.debug(f"MQTT message received on topic: {msg.topic}")
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            ch = payload.get("channel")
            sender = payload.get("sender", "?")
            text = payload.get("payload", {}).get("text")
            ts = datetime.now(pytz.timezone(timezone)).strftime("%I:%M %p %Z")

            if not text:
                logging.debug("Skipping message: no text content.")
                return

            if watch_channels and ch not in watch_channels:
                logging.debug(f"Ignoring message from channel {ch}, not in WATCH_CHANNELS.")
                return

            content = f"📡 [{ch}] {sender} @ {ts}: {text}"
            logging.info(f"Forwarding to Discord: {content}")
            response = requests.post(webhook_url, json={"content": content})

            if response.status_code != 204:
                logging.warning(f"Discord webhook responded with status {response.status_code}")

        except Exception as e:
            logging.error(f"Error handling MQTT message: {e}")

    client.on_connect = on_connect
    client.on_message = on_message

    logging.info(f"Attempting MQTT connection to {broker}:{port}...")
    try:
        client.connect(broker, port, 60)
        logging.info("MQTT connect() called successfully.")
        client.loop_start()
    except Exception as e:
        logging.error(f"MQTT connection failed: {e}")