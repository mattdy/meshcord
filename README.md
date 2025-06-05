# Meshcord

[![Meshcord Banner](https://imgur.com/6WAbb44.png)](https://hub.docker.com/r/mmagtech/meshcord)

**Meshcord** is a lightweight MQTT-to-Discord alert system designed specifically for Meshtastic. It listens for incoming messages on specified Meshtastic channels (via MQTT) and sends formatted notifications to a Discord channel using a webhook. Ideal for users who want real-time mesh alerts delivered to their phone or desktop via Discord — no need to carry your node 24/7!

---

## 🚀 Features

- 🛰️ Monitors multiple Meshtastic channels  
- 📡 Sends alerts to a Discord channel via webhook  
- 🔒 Runs locally on your network (no cloud dependencies)  
- 🧠 Requires no Discord bot setup — just a webhook  
- 🐳 Official Docker image available  
- 🧩 Supports Unraid with custom icon

---

## 🐳 Docker Deployment

👉 **Official Docker Image**:  
**[mmagtech/meshcord on Docker Hub](https://hub.docker.com/r/mmagtech/meshcord)**

### Quick Start (Docker CLI)

```bash
docker run -d \
  --name meshcord \
  -e DISCORD_WEBHOOK_URL="your_webhook_url" \
  -e MQTT_BROKER="192.168.1.10" \
  -e MQTT_PORT="1883" \
  -e CHANNELS="1:Chat,2:Alerts" \
  -e TIMEZONE="America/New_York" \
  mmagtech/meshcord
```

---

### Unraid Users

Use the following as the **container icon**:  
📎 `https://imgur.com/6WAbb44.png`

---

## ⚙️ Environment Variables

| Variable               | Description                                         | Required |
|------------------------|-----------------------------------------------------|----------|
| `DISCORD_WEBHOOK_URL`  | Webhook URL from your Discord server                | ✅       |
| `MQTT_BROKER`          | IP address of your MQTT broker                      | ✅       |
| `MQTT_PORT`            | MQTT broker port (default: 1883)                    | ✅       |
| `CHANNELS`             | Comma-separated list of `channel_number:name`       | ✅       |
| `TIMEZONE`             | Timezone (e.g., `America/New_York`)                 | ✅       |
| `LOGLEVEL`             | Logging level (e.g. `DEBUG`, default: `INFO`)       | ❌       |

---

## 📡 MQTT Configuration (Home Node)

To monitor your mesh network from home:

1. Connect your Meshtastic node to Wi-Fi.
2. Go to the Meshtastic Web UI:
   - Enable **MQTT**
   - Set `MQTT Server Address` to your broker IP (e.g., `192.168.1.10`)
   - Set `Root topic` to `meshtastic` (or keep default)
3. On the desired channels:
   - Enable **Uplink** (✅ Required)
   - Leave **Downlink** disabled (✅ Not required)
   - MQTT channel name **does not need to be** `mqtt`

---

## 💡 Use Case

You’re away from home without your Meshtastic node.  
Someone sends a message to your shared channel via LoRa.  
Your home node receives it and Meshcord sends a formatted alert to Discord.  
Boom — you’re in the loop in real time.

---

## 📦 Local Build (Optional)

```bash
docker build -t meshcord .
```
