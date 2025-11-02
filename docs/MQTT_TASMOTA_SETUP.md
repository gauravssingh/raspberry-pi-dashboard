# Complete Tasmota ESP32 Setup Guide

## Overview

This guide covers the complete setup process for connecting Tasmota ESP32 devices to your Raspberry Pi Dashboard via MQTT. Follow these steps in order for a working configuration.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Raspberry Pi Configuration](#raspberry-pi-configuration)
3. [ESP32 Tasmota Configuration](#esp32-tasmota-configuration)
4. [GPIO/Relay Configuration](#gpriorelay-configuration)
5. [Dashboard Configuration](#dashboard-configuration)
6. [Testing & Verification](#testing--verification)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Required
- Raspberry Pi (3B or newer) with network connection
- ESP32 device with Tasmota firmware installed
- Both devices on the same network

### Software Required
- Raspberry Pi Dashboard installed and running
- Tasmota firmware 8.0+ on ESP32
- Network access to both devices

---

## Raspberry Pi Configuration

### Step 1: Install Mosquitto MQTT Broker

```bash
# Update package list
sudo apt update

# Install Mosquitto broker and clients
sudo apt install -y mosquitto mosquitto-clients

# Enable and start the service
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Verify it's running
sudo systemctl status mosquitto
```

Expected output:
```
● mosquitto.service - Mosquitto MQTT Broker
     Loaded: loaded
     Active: active (running)
```

### Step 2: Configure Mosquitto for Local Network

Create configuration file:

```bash
sudo nano /etc/mosquitto/conf.d/local.conf
```

Add these lines:

```conf
# Listen on all interfaces
listener 1883

# Allow anonymous connections (for local network)
allow_anonymous true

# Optional: Enable logging for troubleshooting
log_dest file /var/log/mosquitto/mosquitto.log
log_type all
```

**For Production (with authentication):**

```bash
# Create password file
sudo mosquitto_passwd -c /etc/mosquitto/passwd mqtt_user

# Update configuration
sudo nano /etc/mosquitto/conf.d/local.conf
```

```conf
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
```

### Step 3: Restart Mosquitto

```bash
sudo systemctl restart mosquitto

# Verify it's listening
sudo netstat -tulpn | grep 1883
```

Expected output:
```
tcp        0      0 0.0.0.0:1883            0.0.0.0:*               LISTEN
```

### Step 4: Get Your Pi's IP Address

```bash
hostname -I | awk '{print $1}'
```

**Note this IP address** - you'll need it for ESP32 configuration (e.g., `192.168.68.65`)

### Step 5: Test MQTT Broker

In one terminal:
```bash
mosquitto_sub -h localhost -t "test/topic" -v
```

In another terminal:
```bash
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"
```

You should see "Hello MQTT" in the first terminal.

---

## ESP32 Tasmota Configuration

### Step 1: Access Tasmota Web Interface

1. Find your ESP32's IP address:
   - Check your router's connected devices
   - Or use: `http://tasmota-XXXXXX.local` (where XXXXXX is part of MAC address)

2. Open in web browser: `http://192.168.68.58` (use your actual IP)

### Step 2: Configure MQTT Settings

1. Go to **Configuration → Configure MQTT**

2. Fill in the following fields:

```
┌─────────────────────────────────────────────┐
│ MQTT Parameters                             │
├─────────────────────────────────────────────┤
│ Host:         192.168.68.65                 │  ← Your Pi's IP
│ Port:         1883                          │  ← Default MQTT port
│ Client:       esp32_tasmota1                │  ← Unique client name
│ User:         (leave blank or use mqtt_user)│  ← If auth enabled
│ Password:     (leave blank or use password) │  ← If auth enabled
│ Topic:        tasmota_0E09CC                │  ← Device identifier
│ Full Topic:   %topic%/%prefix%/             │  ← IMPORTANT: Use this format
└─────────────────────────────────────────────┘
```

**Critical Settings:**

- **Host**: Your Raspberry Pi's IP address (NOT "localhost" or empty)
- **Port**: `1883` (standard MQTT port)
- **Client**: Unique name for this device (no spaces)
- **Topic**: Unique identifier for this device (matches device MAC or your choice)
- **Full Topic**: MUST be `%topic%/%prefix%/` (not `%prefix%/%topic%/`)

### Step 3: Save and Restart

1. Click **Save**
2. Device will restart automatically
3. Wait 15-30 seconds for reconnection

### Step 4: Verify MQTT Connection

Access: `http://192.168.68.58/cm?cmnd=Status%2011`

Look for:
```json
"StatusMQT": {
  "MqttHost": "192.168.68.65",
  "MqttPort": 1883,
  "MqttCount": 1    ← Should be > 0 (means connected)
}
```

**If MqttCount is 0**, device is NOT connected - check your configuration.

---

## GPIO/Relay Configuration

### Step 1: Identify Your ESP32 GPIOs

Common ESP32-DevKit GPIOs for relays:
- GPIO 2 (built-in LED)
- GPIO 4, 5, 12-19, 21-23, 25-27, 32-33

**Avoid:** GPIO 0, 1, 3, 6-11 (used for boot/flash)

### Step 2: Configure Module

1. Go to **Configuration → Configure Module**

2. Select module type:
   - If using plain ESP32-DevKit, select **Generic (18)**
   - Or select specific module if you know it

3. Save and wait for restart

### Step 3: Configure GPIO Pins

1. Go to **Configuration → Configure Module** (again, after restart)

2. Assign GPIOs as relays:

```
GPIO Selection:
┌────────┬─────────────────┬──────────────┐
│ GPIO # │ Assignment      │ Description  │
├────────┼─────────────────┼──────────────┤
│ GPIO2  │ Relay 1         │ First relay  │
│ GPIO4  │ Relay 2         │ Second relay │
│ GPIO5  │ Relay 3         │ Third relay  │
│ GPIO18 │ Button 1        │ Physical btn │
│ GPIO19 │ LED 1           │ Status LED   │
└────────┴─────────────────┴──────────────┘
```

**Example Configuration:**
- For a single relay on GPIO2: Set GPIO2 to **Relay 1**
- For LED control on GPIO2: Set GPIO2 to **Relay 1** (works same way)
- For multiple relays: Assign Relay 1, Relay 2, etc. to different GPIOs

3. Click **Save**
4. Device will restart

### Step 4: Test GPIO Control

Via web console:
```
http://192.168.68.58/cm?cmnd=Power%20ON
http://192.168.68.58/cm?cmnd=Power%20OFF
http://192.168.68.58/cm?cmnd=Power%20TOGGLE
```

Via MQTT:
```bash
# Turn ON
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power" -m "ON"

# Turn OFF
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power" -m "OFF"

# For specific relay (if multiple)
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power1" -m "ON"
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power2" -m "ON"
```

### Hardware Wiring Example (Relay Module)

```
ESP32-DevKit          Relay Module
┌──────────┐         ┌──────────┐
│          │         │          │
│  GPIO2   ├─────────┤ IN       │
│  GND     ├─────────┤ GND      │
│  VIN(5V) ├─────────┤ VCC      │
│          │         │          │
└──────────┘         └──────────┘
```

**For LEDs:**
```
ESP32      Resistor    LED
GPIO2 ─────[220Ω]────►|────┐
                           │
GND ───────────────────────┘
```

---

## Dashboard Configuration

### Step 1: Restart Dashboard Service

```bash
sudo systemctl restart dashboard
```

### Step 2: Access MQTT Page

Open in browser: `http://192.168.68.65/mqtt`

### Step 3: Connect to MQTT Broker

1. Click **⚙️ Configure** button
2. Verify settings:
   ```
   Broker Host: localhost
   Broker Port: 1883
   Username: (blank or your username)
   Password: (blank or your password)
   ```
3. Click **Save Configuration**
4. Click **Connect** button
5. Status should show: 🟢 **Connected**

### Step 4: Add Your ESP32 Device

1. Click **+ Add Device**
2. Fill in device details:
   ```
   Device Name: ESP32 Living Room
   MQTT Topic: tasmota_0E09CC        ← MUST match Tasmota Topic
   Device Type: switch (or light/rgb as appropriate)
   Description: ESP32 relay controller
   ```
3. Click **Add Device**

### Step 5: Verify Device Status

After a few seconds, the device card should show:
- Status: 🟢 **ONLINE**
- Last seen timestamp
- Power state (ON/OFF)

If it shows OFFLINE:
- Wait 30 seconds (for telemetry)
- Click browser refresh
- Check troubleshooting section below

---

## Testing & Verification

### Test 1: Dashboard Controls

In the dashboard:
1. Click **ON** button → Device should turn on
2. Click **OFF** button → Device should turn off
3. Click **TOGGLE** button → Device should toggle state

### Test 2: MQTT Direct Control

```bash
# Subscribe to all device messages
mosquitto_sub -h localhost -t "tasmota_0E09CC/#" -v &

# Send commands
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power" -m "TOGGLE"

# You should see response messages like:
# tasmota_0E09CC/stat/RESULT {"POWER":"ON"}
```

### Test 3: API Control

```bash
# Turn ON via API
curl -X POST http://localhost/api/mqtt/power/tasmota_0E09CC \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'

# Turn OFF via API
curl -X POST http://localhost/api/mqtt/power/tasmota_0E09CC \
  -H "Content-Type: application/json" \
  -d '{"action": "off"}'

# Get device status
curl http://localhost/api/mqtt/devices/tasmota_0E09CC | python3 -m json.tool
```

### Test 4: Verify End-to-End

Complete verification checklist:

```bash
# 1. Check Mosquitto is running
sudo systemctl status mosquitto

# 2. Check ESP32 MQTT connection
curl -s "http://192.168.68.58/cm?cmnd=Status%2011" | grep MqttCount
# Should show: "MqttCount":1 or higher

# 3. Check dashboard connection
curl http://localhost/api/mqtt/status | grep connected
# Should show: "connected": true

# 4. Monitor MQTT traffic
mosquitto_sub -h localhost -t "#" -v | grep tasmota_0E09CC
# Should show messages from your device
```

---

## Troubleshooting

### Issue: Device Shows OFFLINE in Dashboard

**Possible Causes:**

1. **Topic Format Mismatch**
   ```bash
   # Check Tasmota Full Topic setting
   curl "http://192.168.68.58/cm?cmnd=FullTopic"
   
   # Should return: {"FullTopic":"%topic%/%prefix%/"}
   # If not, fix it:
   curl "http://192.168.68.58/cm?cmnd=FullTopic%20%25topic%25/%25prefix%25/"
   ```

2. **MQTT Host Not Set**
   ```bash
   # Check MQTT Host
   curl "http://192.168.68.58/cm?cmnd=MqttHost"
   
   # Should show your Pi's IP
   # If empty, set it:
   curl "http://192.168.68.58/cm?cmnd=MqttHost%20192.168.68.65"
   curl "http://192.168.68.58/cm?cmnd=Restart%201"
   ```

3. **Dashboard Not Connected**
   ```bash
   # Reconnect dashboard
   curl -X POST http://localhost/api/mqtt/disconnect
   sleep 2
   curl -X POST http://localhost/api/mqtt/connect
   ```

4. **Wrong Topic in Dashboard**
   - Dashboard topic MUST exactly match Tasmota topic
   - Check: `curl http://localhost/api/mqtt/devices`
   - Compare with: `curl "http://192.168.68.58/cm?cmnd=Topic"`

### Issue: MqttCount is 0 (Not Connected)

**Check Mosquitto:**
```bash
# Is Mosquitto running?
sudo systemctl status mosquitto

# Is it listening on port 1883?
sudo netstat -tulpn | grep 1883

# Check logs
sudo tail -50 /var/log/mosquitto/mosquitto.log
```

**Check ESP32:**
```bash
# Get full status
curl "http://192.168.68.58/cm?cmnd=Status%200" | python3 -m json.tool

# Look for:
# - MqttHost (should be your Pi's IP)
# - MqttPort (should be 1883)
# - MqttCount (should be > 0)
```

**Fix Steps:**
```bash
# 1. Ensure Mosquitto allows connections
sudo nano /etc/mosquitto/conf.d/local.conf
# Add: allow_anonymous true
# Add: listener 1883

# 2. Restart Mosquitto
sudo systemctl restart mosquitto

# 3. Restart ESP32
curl "http://192.168.68.58/cm?cmnd=Restart%201"

# 4. Wait 30 seconds and check again
sleep 30
curl "http://192.168.68.58/cm?cmnd=Status%2011" | grep MqttCount
```

### Issue: Commands Not Working

**Test MQTT Path:**
```bash
# Subscribe to all messages
mosquitto_sub -h localhost -t "#" -v &

# Send test command
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power" -m "TOGGLE"

# You should see:
# - Your command: tasmota_0E09CC/cmnd/Power TOGGLE
# - Response: tasmota_0E09CC/stat/RESULT {"POWER":"ON"}
```

**If no response:**
- ESP32 is not subscribed (MqttCount = 0)
- Topic name is wrong
- Mosquitto is not routing messages

### Issue: Relay Not Switching

1. **GPIO Not Configured**
   - Go to Configuration → Configure Module
   - Assign GPIO to Relay 1 (or 2, 3, etc.)
   - Save and restart

2. **Test Via Web Interface**
   ```
   http://192.168.68.58/cm?cmnd=Power%20ON
   ```
   - If this works, MQTT works, problem is dashboard
   - If this doesn't work, GPIO not configured

3. **Check Hardware Wiring**
   - Verify relay module connections
   - Check power supply (relay modules need 5V)
   - Test relay with multimeter

### Issue: Authentication Errors

If using Mosquitto with authentication:

```bash
# Test with credentials
mosquitto_sub -h localhost -u mqtt_user -P your_password -t "#" -v

# Update dashboard configuration
curl -X POST http://localhost/api/mqtt/config \
  -H "Content-Type: application/json" \
  -d '{
    "broker": {
      "host": "localhost",
      "port": 1883,
      "username": "mqtt_user",
      "password": "your_password"
    }
  }'

# Update Tasmota
# Via web interface: Configuration → Configure MQTT
# Set User and Password fields
```

---

## Configuration Summary

### Raspberry Pi (Mosquitto)
```conf
# /etc/mosquitto/conf.d/local.conf
listener 1883
allow_anonymous true
```

### ESP32 (Tasmota)
```
Host:       192.168.68.65        # Your Pi's IP
Port:       1883
Client:     esp32_tasmota1       # Unique name
Topic:      tasmota_0E09CC       # Device identifier
Full Topic: %topic%/%prefix%/    # Required format
```

### Dashboard (MQTT Config)
```json
{
  "broker": {
    "host": "localhost",
    "port": 1883
  },
  "devices": [
    {
      "name": "ESP32 Living Room",
      "topic": "tasmota_0E09CC",
      "device_type": "switch"
    }
  ]
}
```

---

## Quick Setup Checklist

- [ ] Mosquitto installed on Pi
- [ ] Mosquitto configured to allow connections
- [ ] Mosquitto service running
- [ ] ESP32 has Tasmota firmware
- [ ] ESP32 connected to WiFi
- [ ] ESP32 MQTT Host set to Pi's IP
- [ ] ESP32 MQTT Full Topic set to `%topic%/%prefix%/`
- [ ] ESP32 GPIO configured as Relay
- [ ] ESP32 MqttCount > 0 (connected)
- [ ] Dashboard MQTT configured
- [ ] Dashboard connected to broker
- [ ] Device added to dashboard
- [ ] Device shows ONLINE
- [ ] Controls working (ON/OFF/TOGGLE)

---

## Advanced Topics

### Multiple Relays

For devices with multiple relays:

```bash
# Control specific relays
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power1" -m "ON"
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power2" -m "OFF"

# Via API
curl -X POST http://localhost/api/mqtt/power/tasmota_0E09CC \
  -H "Content-Type: application/json" \
  -d '{"action": "on", "relay": 1}'
```

### RGB LED Control

For RGB LED strips:

```bash
# Set color (hex format)
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Color" -m "FF0000"  # Red

# Via dashboard
curl -X POST http://localhost/api/mqtt/color/tasmota_0E09CC \
  -H "Content-Type: application/json" \
  -d '{"color": "#00FF00"}'  # Green
```

### Dimmer Control

For dimmable lights:

```bash
# Set brightness (0-100%)
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Dimmer" -m "50"

# Via dashboard
curl -X POST http://localhost/api/mqtt/dimmer/tasmota_0E09CC \
  -H "Content-Type: application/json" \
  -d '{"level": 75}'
```

---

## Security Recommendations

### For Local Network Use
- Use firewall to restrict MQTT port 1883 to local network only
- Consider VPN for remote access

### For Internet-Exposed Systems
1. Enable Mosquitto authentication
2. Use TLS/SSL encryption
3. Change default ports
4. Implement certificate-based authentication
5. Regular firmware updates

See [MQTT_TASMOTA_GUIDE.md](MQTT_TASMOTA_GUIDE.md) for detailed security setup.

---

## Reference Commands

### Useful Mosquitto Commands
```bash
# Monitor all MQTT traffic
mosquitto_sub -h localhost -t "#" -v

# Monitor specific device
mosquitto_sub -h localhost -t "tasmota_0E09CC/#" -v

# Send command
mosquitto_pub -h localhost -t "tasmota_0E09CC/cmnd/Power" -m "TOGGLE"

# Check broker status
sudo systemctl status mosquitto

# View logs
sudo tail -f /var/log/mosquitto/mosquitto.log
```

### Useful Tasmota Commands
```bash
# Get all status
curl "http://192.168.68.58/cm?cmnd=Status%200"

# Get MQTT status
curl "http://192.168.68.58/cm?cmnd=Status%2011"

# Get topic
curl "http://192.168.68.58/cm?cmnd=Topic"

# Get full topic format
curl "http://192.168.68.58/cm?cmnd=FullTopic"

# Restart device
curl "http://192.168.68.58/cm?cmnd=Restart%201"
```

### Useful Dashboard API Commands
```bash
# Get MQTT status
curl http://localhost/api/mqtt/status | python3 -m json.tool

# List devices
curl http://localhost/api/mqtt/devices | python3 -m json.tool

# Control device
curl -X POST http://localhost/api/mqtt/power/tasmota_0E09CC \
  -H "Content-Type: application/json" \
  -d '{"action": "toggle"}'
```

---

## Support

For additional help:
- Dashboard logs: `/home/gauravs/dashboard/logs/app.log`
- Mosquitto logs: `/var/log/mosquitto/mosquitto.log`
- Tasmota console: `http://192.168.68.58/cs` (Console menu)

---

*Last updated: November 2, 2025*
*Tested with: Raspberry Pi 3B, ESP32-DevKit, Tasmota 15.1.0*

