# MQTT Quick Start Guide

## 5-Minute Setup for Tasmota Devices

This guide will get you up and running with MQTT and Tasmota devices in 5 minutes.

> **📚 For Complete Setup with GPIO/Relay Configuration:** See [MQTT_TASMOTA_SETUP.md](MQTT_TASMOTA_SETUP.md) for the comprehensive guide including GPIO pin configuration, relay setup, and detailed troubleshooting.

## Prerequisites

- Raspberry Pi with the Dashboard installed
- ESP32 device flashed with Tasmota firmware
- Both devices on the same network

## Step 1: Install MQTT Broker (2 minutes)

On your Raspberry Pi, run:

```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

Verify it's running:
```bash
sudo systemctl status mosquitto
```

## Step 2: Configure Tasmota Device (2 minutes)

1. Find your Tasmota device's IP address (check your router or use http://tasmota-XXXX.local)
2. Open the Tasmota web interface in your browser
3. Go to **Configuration → Configure MQTT**
4. Set these values:
   - **Host**: Your Raspberry Pi's IP (e.g., `192.168.1.100`)
   - **Port**: `1883`
   - **Topic**: A unique name (e.g., `tasmota_device1`)
   - Leave username/password blank for now
5. Click **Save** (device will restart)

## Step 3: Add Device to Dashboard (1 minute)

1. Open your Raspberry Pi Dashboard
2. Click **📡 MQTT/IoT** from the home page
3. Click **Connect** (uses default localhost:1883)
4. Click **+ Add Device**
5. Fill in:
   - **Device Name**: "My First Device"
   - **MQTT Topic**: `tasmota_device1` (must match Tasmota)
   - **Device Type**: Select appropriate type
6. Click **Add Device**

## Step 4: Test It!

You should now see your device card. Try clicking:
- **ON** button to turn on
- **OFF** button to turn off
- **TOGGLE** to switch state

The device should respond immediately!

## Troubleshooting

**Device shows offline?**
- Verify Tasmota shows "Connected" in its web console
- Check that the Topic in Tasmota matches the dashboard exactly
- **CRITICAL:** Ensure Full Topic is `%topic%/%prefix%/` (not `%prefix%/%topic%/`)
- Make sure Mosquitto is running: `sudo systemctl status mosquitto`

**Commands not working?**
- Test MQTT manually:
  ```bash
  # Subscribe to all messages
  mosquitto_sub -h localhost -t "#" -v
  
  # In another terminal, send a test command
  mosquitto_pub -h localhost -t "tasmota_device1/cmnd/Power" -m "ON"
  ```

**For detailed troubleshooting and GPIO/relay setup:** See [MQTT_TASMOTA_SETUP.md](MQTT_TASMOTA_SETUP.md)

## Next Steps

- Add more devices following the same process
- Explore advanced controls (dimmer, RGB colors)
- Set up authentication for security (see full MQTT_TASMOTA_GUIDE.md)
- Configure automatic device startup

## Quick Commands Reference

**Turn device ON:**
```bash
mosquitto_pub -h localhost -t "tasmota_device1/cmnd/Power" -m "ON"
```

**Turn device OFF:**
```bash
mosquitto_pub -h localhost -t "tasmota_device1/cmnd/Power" -m "OFF"
```

**Get status:**
```bash
mosquitto_pub -h localhost -t "tasmota_device1/cmnd/Status" -m "0"
```

**Monitor all messages:**
```bash
mosquitto_sub -h localhost -t "#" -v
```

## That's It!

You now have MQTT-controlled IoT devices integrated with your Raspberry Pi Dashboard. For more advanced features, see [MQTT_TASMOTA_GUIDE.md](MQTT_TASMOTA_GUIDE.md).

---

**Tip**: Name your devices clearly (e.g., "Kitchen Light", "Bedroom Fan") and use consistent topic naming (e.g., `tasmota_kitchen_light`) for easy management.

