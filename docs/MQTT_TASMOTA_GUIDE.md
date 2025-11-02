# MQTT/IoT Device Control Guide

## Overview

This guide explains how to set up and use MQTT support in the Raspberry Pi Dashboard to control Tasmota ESP32 devices and other IoT sensors.

## What is MQTT?

MQTT (Message Queuing Telemetry Transport) is a lightweight messaging protocol ideal for IoT devices. It uses a publish-subscribe model where:
- **Broker**: Central server that routes messages (runs on your Raspberry Pi)
- **Clients**: Devices that publish or subscribe to topics (your ESP32 devices)
- **Topics**: Channels for organizing messages (e.g., `tasmota_bedroom/power`)

## What is Tasmota?

Tasmota is an open-source firmware for ESP8266/ESP32 devices that provides MQTT support out-of-the-box. It's commonly used for:
- Smart switches and relays
- Smart lights (including RGB)
- Sensors (temperature, humidity, motion, etc.)
- Custom IoT projects

## Architecture

```
┌─────────────────┐      MQTT       ┌──────────────────┐
│  Raspberry Pi   │◄───────────────►│  Mosquitto       │
│  Dashboard      │                 │  MQTT Broker     │
│                 │                 │                  │
└─────────────────┘                 └──────────────────┘
                                            ▲
                                            │ MQTT
                                            ├──────────────┐
                                            │              │
                                    ┌───────▼─────┐  ┌────▼──────┐
                                    │  ESP32 #1   │  │  ESP32 #2 │
                                    │  (Tasmota)  │  │  (Tasmota)│
                                    │             │  │           │
                                    │  Relay      │  │  RGB LED  │
                                    └─────────────┘  └───────────┘
```

## Installation

### 1. Install Mosquitto MQTT Broker

First, install the Mosquitto MQTT broker on your Raspberry Pi:

```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
```

Enable and start the service:

```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

Verify it's running:

```bash
sudo systemctl status mosquitto
```

### 2. Configure Mosquitto (Optional)

For basic setup, Mosquitto works out-of-the-box. For production use, you should configure authentication:

```bash
# Create a password file
sudo mosquitto_passwd -c /etc/mosquitto/passwd your_username

# Edit the configuration
sudo nano /etc/mosquitto/mosquitto.conf
```

Add these lines:

```
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
```

Restart Mosquitto:

```bash
sudo systemctl restart mosquitto
```

### 3. Dependencies Already Installed

The Python MQTT client (`paho-mqtt`) has already been installed for you.

## Tasmota Device Setup

### 1. Flash Tasmota Firmware

If your ESP32 doesn't have Tasmota yet:

1. Download Tasmota firmware from: https://github.com/arendst/Tasmota
2. Use ESPHome-Flasher or esptool.py to flash your ESP32
3. Connect to the Tasmota WiFi AP and configure your network

### 2. Configure MQTT in Tasmota

Access your Tasmota device's web interface (usually `http://tasmota-XXXX.local`):

1. Go to **Configuration → Configure MQTT**
2. Set the following:
   - **Host**: Your Raspberry Pi's IP address (e.g., `192.168.1.100`)
   - **Port**: `1883` (default MQTT port)
   - **Client**: Unique name (e.g., `tasmota_bedroom`)
   - **User**: Your MQTT username (if authentication enabled)
   - **Password**: Your MQTT password (if authentication enabled)
   - **Topic**: A unique topic name (e.g., `tasmota_bedroom`)
   - **Full Topic**: Leave as default `%prefix%/%topic%/`

3. Click **Save** and the device will restart

### 3. Test MQTT Connection

From your Raspberry Pi, subscribe to all Tasmota messages:

```bash
mosquitto_sub -h localhost -t "tasmota_bedroom/#" -v
```

You should see messages when the device connects and sends updates.

## Dashboard Configuration

### 1. Access the MQTT Control Page

Navigate to the MQTT/IoT section from your dashboard home page (📡 MQTT/IoT link).

### 2. Configure MQTT Broker

1. Click **⚙️ Configure** button
2. Enter your broker settings:
   - **Broker Host/IP**: `localhost` (or your Pi's IP if accessing remotely)
   - **Broker Port**: `1883`
   - **Username**: (optional, if you configured authentication)
   - **Password**: (optional, if you configured authentication)
3. Click **Save Configuration**

### 3. Connect to Broker

Click the **Connect** button. The status indicator should turn green (🟢) when connected.

### 4. Add Your Tasmota Devices

1. Click **+ Add Device**
2. Fill in device details:
   - **Device Name**: Friendly name (e.g., "Living Room Light")
   - **MQTT Topic**: The topic you set in Tasmota (e.g., `tasmota_bedroom`)
   - **Device Type**: Select appropriate type (Switch, Light, RGB, Sensor, Generic)
   - **Description**: Optional description
3. Click **Add Device**

## Using the Dashboard

### Basic Controls

Each device card shows:
- **Device name** and status (Online/Offline)
- **Topic** (the MQTT topic)
- **Last seen** timestamp
- **Control buttons**:
  - **ON**: Turn device on
  - **OFF**: Turn device off
  - **TOGGLE**: Toggle power state
  - **More...**: Advanced controls
  - **🗑️**: Remove device

### Advanced Controls

Click **More...** to access device-specific controls:

**For Lights/Dimmers:**
- Adjust brightness (0-100%)
- Set dimmer level

**For RGB Lights:**
- Choose color with color picker
- Set RGB values

**For All Devices:**
- Request status update
- Restart device

## Tasmota Commands Reference

The dashboard sends standard Tasmota commands via MQTT. Here are common commands:

### Power Control
- `Power ON` / `Power OFF` / `Power TOGGLE`
- `Power1 ON` (for multi-relay devices)

### Dimmer Control (for dimmable lights)
- `Dimmer 50` (set to 50%)
- `Dimmer +10` (increase by 10%)
- `Dimmer -10` (decrease by 10%)

### Color Control (for RGB lights)
- `Color FF0000` (Red)
- `Color 00FF00` (Green)
- `Color 0000FF` (Blue)
- `Color FFFFFF` (White)

### Status Requests
- `Status 0` (all status)
- `Status 1` (device parameters)
- `Status 2` (firmware version)

### System Commands
- `Restart 1` (restart device)
- `Reset 1` (reset to defaults - use with caution!)

## MQTT Topics Explained

Tasmota uses a structured topic format:

```
<topic_prefix>/<topic>/<command>
```

### Topic Prefixes
- `cmnd/` - Commands sent TO the device
- `stat/` - Status responses FROM the device
- `tele/` - Telemetry data FROM the device

### Examples
If your device topic is `tasmota_bedroom`:

- `cmnd/tasmota_bedroom/Power` - Send power command
- `stat/tasmota_bedroom/RESULT` - Device status response
- `tele/tasmota_bedroom/STATE` - Telemetry state updates
- `tele/tasmota_bedroom/SENSOR` - Sensor data (if available)
- `tele/tasmota_bedroom/LWT` - Last Will and Testament (online/offline)

## Troubleshooting

### Device Shows as Offline

1. **Check Tasmota connection**:
   ```bash
   mosquitto_sub -h localhost -t "tasmota_bedroom/tele/LWT" -v
   ```
   Should show "Online"

2. **Verify MQTT settings** in Tasmota web interface

3. **Check broker is running**:
   ```bash
   sudo systemctl status mosquitto
   ```

4. **Check firewall** (if applicable):
   ```bash
   sudo ufw allow 1883/tcp
   ```

### Commands Not Working

1. **Check topic name** matches exactly between dashboard and Tasmota
2. **Verify permissions** if using authentication
3. **Monitor MQTT traffic**:
   ```bash
   mosquitto_sub -h localhost -t "#" -v
   ```
   This shows all MQTT messages

### Connection Refused

1. **Check broker is running** on port 1883
2. **Verify credentials** if authentication is enabled
3. **Check network connectivity** between Pi and ESP32

### Dashboard Not Connecting

1. **Check configuration** - ensure correct broker host/port
2. **Review logs**:
   ```bash
   tail -f /home/gauravs/dashboard/logs/app.log
   ```
3. **Restart dashboard service**:
   ```bash
   sudo systemctl restart dashboard
   ```

## Security Best Practices

### 1. Enable MQTT Authentication

Always use username/password authentication in production:

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd mqtt_user
```

### 2. Use TLS/SSL (Advanced)

For remote access, consider enabling TLS:

1. Generate certificates
2. Configure Mosquitto with TLS
3. Update Tasmota devices with TLS settings

### 3. Network Segmentation

Consider putting IoT devices on a separate VLAN for security.

### 4. Firewall Rules

Only expose MQTT port (1883) to trusted networks:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 1883
```

## Advanced Features

### Auto-Discovery

The dashboard subscribes to `tasmota/discovery/#` topics for automatic device discovery (future feature).

### Custom Commands

You can send any Tasmota command using the API:

```bash
curl -X POST http://your-pi-ip/api/mqtt/command \
  -H "Content-Type: application/json" \
  -d '{
    "device_topic": "tasmota_bedroom",
    "command": "Status",
    "payload": "0"
  }'
```

### Multiple Relays

For devices with multiple relays, use:
- `Power1`, `Power2`, `Power3`, etc.

### Timers and Schedules

Configure timers in Tasmota web interface for scheduled operations.

## Configuration Files

### MQTT Configuration
Located at: `/home/gauravs/dashboard/configs/mqtt_config.json`

Example:
```json
{
  "broker": {
    "host": "localhost",
    "port": 1883,
    "username": "mqtt_user",
    "password": "your_password",
    "auto_connect": true
  },
  "devices": [
    {
      "name": "Living Room Light",
      "topic": "tasmota_living_room",
      "device_type": "light",
      "description": "Main ceiling light"
    }
  ],
  "settings": {
    "discovery_enabled": true,
    "retain_messages": false,
    "qos": 1
  }
}
```

## API Reference

### Get MQTT Status
```bash
GET /api/mqtt/status
```

### Connect to Broker
```bash
POST /api/mqtt/connect
```

### Get Devices
```bash
GET /api/mqtt/devices
```

### Add Device
```bash
POST /api/mqtt/devices
Content-Type: application/json

{
  "name": "Device Name",
  "topic": "tasmota_topic",
  "device_type": "switch"
}
```

### Control Power
```bash
POST /api/mqtt/power/{device_topic}
Content-Type: application/json

{
  "action": "on"  // or "off" or "toggle"
}
```

### Send Custom Command
```bash
POST /api/mqtt/command
Content-Type: application/json

{
  "device_topic": "tasmota_topic",
  "command": "Status",
  "payload": "0"
}
```

## Example Projects

### 1. Smart Light Control
- **Hardware**: ESP32 + Relay module + LED bulb
- **Use Case**: Control bedroom light from dashboard
- **Setup**: Flash Tasmota, configure GPIO for relay, add to dashboard

### 2. Temperature Monitoring
- **Hardware**: ESP32 + DHT22 sensor
- **Use Case**: Monitor room temperature/humidity
- **Setup**: Configure Tasmota sensor, view telemetry in dashboard

### 3. Smart Switch
- **Hardware**: ESP32 + Relay + Physical switch
- **Use Case**: Control appliances remotely
- **Setup**: Configure Tasmota with button GPIO, add to dashboard

### 4. RGB LED Strip
- **Hardware**: ESP32 + RGB LED strip
- **Use Case**: Mood lighting with color control
- **Setup**: Configure Tasmota for RGB, use color picker in dashboard

## Further Reading

- **Tasmota Documentation**: https://tasmota.github.io/docs/
- **MQTT.org**: https://mqtt.org/
- **Mosquitto Documentation**: https://mosquitto.org/documentation/
- **ESP32 Pinout**: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/

## Support

For issues or questions:
1. Check the logs: `/home/gauravs/dashboard/logs/app.log`
2. Test MQTT directly with mosquitto_pub/sub
3. Verify Tasmota console output
4. Review this documentation

---

**Note**: Always test new devices in a safe environment before deploying in production. IoT devices should be properly secured and monitored.

