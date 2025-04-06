
import os
import json
import requests
from dotenv import load_dotenv
from mqtt_interface_webhook import register_mqtt_listener

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL is not set in .env")

def send_to_discord(content):
    data = {
        "username": "Mesh Watchdog",
        "content": content
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"⚠️ Failed to send message to Discord: {response.status_code} - {response.text}")

register_mqtt_listener(send_to_discord)
