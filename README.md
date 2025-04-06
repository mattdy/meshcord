# Mesh Watchdog — Webhook Edition 📡

**Mesh Watchdog** is a lightweight, always-on notifier that listens for messages on your **Meshtastic** mesh network and relays them to a **Discord channel** using a simple **webhook**.

It runs locally, alongside your MQTT broker, and notifies you in real time when any of your nodes receive a message. Perfect for home base stations, silent monitors, or anyone who wants to be alerted via Discord without carrying a radio.

---

## 🚀 Features

- 🛰️ Listens for messages from Meshtastic over MQTT
- 🔗 Sends real-time alerts to Discord via webhook
- ⏰ Includes timestamp and sender ID
- ⚙️ Channel filtering support (monitor specific channels)
- 📦 Simple setup with Docker or Python

---

## 🔧 Requirements

- A Meshtastic node with:
  - **MQTT** enabled
  - **Uplink** enabled
- A local **MQTT broker** (e.g., Mosquitto)
- A **Discord Webhook URL**
- Docker or Python 3.9+

---

## 🛠️ Setup

### 1. Create a Discord Webhook

1. Go to your Discord channel settings → **Integrations**
2. Click **New Webhook**
3. Name it (e.g., "Mesh Watchdog")
4. Copy the webhook URL

### 2. Configure `.env`

Create a `.env` file in your project root:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_id/your_token
MQTT_BROKER=mosquitto
MQTT_PORT=1883
TIMEZONE=America/New_York
WATCH_CHANNELS=1,2
```

- `WATCH_CHANNELS` is optional (comma-separated values)
- `TIMEZONE` affects the timestamp format

---

## ▶️ Run the Bot

### With Docker
```bash
docker compose up -d
```

### With Python
```bash
pip install -r requirements.txt
python bot_webhook.py
```

---

## 🧾 Sample Alert

```
📡 [1] !849ade78 @ 06:45 PM EDT: Hello from the mesh!
```

---

## 🌐 Local-Only Design

This bot is designed to run inside your local network. If you plan to access it remotely, you must secure your MQTT broker (e.g., using a VPN or reverse proxy).

---

## 🧠 Why Use This?

If your Meshtastic base node is at home, you can still receive mesh messages via Discord anywhere in the world. No need for a second device in your pocket — just check Discord.

---

## 🪪 License

MIT — Free for personal or commercial use.

---

Built with ❤️ for mesh explorers.

## 📡 MQTT Configuration (for WiFi Node)

The WiFi-connected Meshtastic node (your home base) should have the following settings:

| Setting               | Value                     |
|------------------------|----------------------------|
| MQTT Enabled          | ✅ ON                      |
| Uplink Enabled        | ✅ ON                      |
| Downlink Enabled      | ❌ OFF (not needed)        |
| MQTT Server Address   | `address of broker`             |
| MQTT Port             | `1883` (default)           |
| Root Topic            | `meshtastic` (default)     |
| Uplink Channels       | Match `WATCH_CHANNELS` in `.env` |

> ✅ Channel names do **not** need to be called `mqtt`. You can name them anything (e.g., `Meshages`, `FieldOps`).