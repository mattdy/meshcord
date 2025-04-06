import json
import pytz
import logging
import requests
from datetime import datetime
import paho.mqtt.client as mqtt

client = mqtt.Client()

def setup_mqtt(webhook_url, broker, port, timezone, watch_channels):
    def on_connect(client, userdata, flags, rc):
        logging.info(f"Connected to MQTT broker at {broker}:{port}")
        client.subscribe("meshtastic/2/json/#")

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            ch = payload.get("channel")
            sender = payload.get("sender", "?")
            text = payload.get("payload", {}).get("text")
            ts = datetime.now(pytz.timezone(timezone)).strftime("%I:%M %p %Z")

            if not text or (watch_channels and ch not in watch_channels):
                return

            content = f"📡 [{ch}] {sender} @ {ts}: {text}"
            logging.info(f"Sending alert: {content}")
            requests.post(webhook_url, json={"content": content})

        except Exception as e:
            logging.error(f"Error handling MQTT message: {e}")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_start()