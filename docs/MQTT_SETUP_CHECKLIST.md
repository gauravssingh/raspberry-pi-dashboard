# MQTT Setup Checklist

Use this checklist to verify your MQTT/IoT integration is working correctly.

## ✅ Installation Verification

### 1. Check Dashboard Status
```bash
sudo systemctl status dashboard
```
**Expected**: Active (running) ✅

### 2. Check Python Dependencies
```bash
source /home/gauravs/dashboard/venv/bin/activate
pip list | grep paho-mqtt
```
**Expected**: `paho-mqtt 1.6.1` ✅

### 3. Install Mosquitto Broker (if not done)
```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```
**Expected**: Active (running) ✅

### 4. Test Mosquitto
```bash
# Terminal 1 - Subscribe
mosquitto_sub -h localhost -t "test/topic" -v

# Terminal 2 - Publish (open new terminal)
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"
```
**Expected**: Message appears in Terminal 1 ✅

## ✅ Dashboard Integration

### 5. Access MQTT Page
- Open browser: `http://your-pi-ip/mqtt`
- **Expected**: MQTT control page loads ✅

### 6. Check Configuration
- Click "⚙️ Configure" button
- **Expected**: Modal opens with broker settings ✅
- Verify default settings:
  - Host: `localhost`
  - Port: `1883`

### 7. Connect to Broker
- Click "Connect" button
- **Expected**: 
  - Status changes to 🟢 "Connected"
  - Toast notification: "Connected to MQTT broker!" ✅

### 8. Check API Endpoints
```bash
# Check status
curl http://localhost/api/mqtt/status

# Expected output:
# {"success":true,"connected":true,...}
```
**Expected**: JSON response with success=true ✅

## ✅ Tasmota Device Setup

### 9. Flash Tasmota (if needed)
- Use ESPHome-Flasher or esptool.py
- Connect ESP32 via USB
- Flash Tasmota firmware
**Expected**: Device boots with Tasmota ✅

### 10. Configure Tasmota WiFi
- Connect to Tasmota AP (tasmota-XXXX)
- Configure your WiFi network
- Device connects to network
**Expected**: Device accessible via IP or hostname ✅

### 11. Configure Tasmota MQTT
Access Tasmota web interface → Configuration → Configure MQTT:

- **Host**: `192.168.x.x` (your Pi's IP)
- **Port**: `1883`
- **Client**: `tasmota_device1` (unique name)
- **Topic**: `tasmota_device1` (must match Client)
- **Full Topic**: `%prefix%/%topic%/` (default)

Click **Save** and device restarts.

**Expected**: Device connects to MQTT broker ✅

### 12. Verify Tasmota Connection
```bash
# Subscribe to device messages
mosquitto_sub -h localhost -t "tasmota_device1/#" -v
```
**Expected**: See messages like:
```
tasmota_device1/tele/LWT Online
tasmota_device1/tele/STATE {...}
```
✅

### 13. Test Manual Control
```bash
# Turn ON
mosquitto_pub -h localhost -t "tasmota_device1/cmnd/Power" -m "ON"

# Turn OFF
mosquitto_pub -h localhost -t "tasmota_device1/cmnd/Power" -m "OFF"
```
**Expected**: Device responds to commands ✅

## ✅ Dashboard Device Control

### 14. Add Device to Dashboard
- In dashboard, click "+ Add Device"
- Fill in:
  - **Name**: "Test Device"
  - **Topic**: `tasmota_device1`
  - **Type**: Select appropriate type
- Click "Add Device"

**Expected**: Device card appears ✅

### 15. Check Device Status
**Expected**: Device card shows:
- Device name and topic
- Status: 🟢 Online or 🔴 Offline
- Control buttons enabled ✅

### 16. Test Power Control
- Click "ON" button
**Expected**: 
- Device turns on
- Toast: "Power on command sent"
- Device physically responds ✅

- Click "OFF" button
**Expected**: 
- Device turns off
- Toast: "Power off command sent"
- Device physically responds ✅

- Click "TOGGLE" button
**Expected**: 
- Device toggles state
- Toast: "Power toggle command sent" ✅

### 17. Test Advanced Controls (if applicable)
- Click "More..." button
**Expected**: Modal opens with advanced options ✅

For **Light/Dimmer**:
- Adjust dimmer slider
- Click "Set Dimmer"
**Expected**: Light brightness changes ✅

For **RGB Light**:
- Select color with color picker
- Click "Set Color"
**Expected**: LED color changes ✅

### 18. Test Status Request
- Click "Request Status"
**Expected**: Toast notification, device sends status ✅

### 19. Monitor MQTT Traffic
```bash
# In terminal, watch all messages
mosquitto_sub -h localhost -t "#" -v
```
**Expected**: See commands and responses in real-time ✅

## ✅ Verification Complete

If all items above are checked, your MQTT integration is working perfectly! 🎉

## 🔧 Troubleshooting Failed Checks

### Dashboard Not Loading MQTT Page
```bash
# Check logs
tail -50 /home/gauravs/dashboard/logs/app.log

# Restart service
sudo systemctl restart dashboard
```

### Mosquitto Not Running
```bash
# Check status
sudo systemctl status mosquitto

# Check logs
sudo journalctl -u mosquitto -n 50

# Restart
sudo systemctl restart mosquitto
```

### Tasmota Not Connecting
1. Verify Pi's IP address: `hostname -I`
2. Check Tasmota MQTT settings match
3. Check Tasmota console for errors
4. Try ping from Tasmota to Pi
5. Verify firewall not blocking port 1883

### Device Shows Offline
```bash
# Check if device is publishing
mosquitto_sub -h localhost -t "tasmota_device1/tele/LWT" -v

# Should show: Online
```

### Commands Not Working
```bash
# Check topic is correct
mosquitto_sub -h localhost -t "tasmota_device1/#" -v

# Send test command
mosquitto_pub -h localhost -t "tasmota_device1/cmnd/Power" -m "TOGGLE"
```

## 📚 Quick Reference

### Important Locations
- **Dashboard**: `http://your-pi-ip/mqtt`
- **Config**: `/home/gauravs/dashboard/configs/mqtt_config.json`
- **Logs**: `/home/gauravs/dashboard/logs/app.log`
- **Docs**: `/home/gauravs/dashboard/docs/MQTT_*.md`

### Quick Commands
```bash
# Restart dashboard
sudo systemctl restart dashboard

# Restart Mosquitto
sudo systemctl restart mosquitto

# View live logs
tail -f /home/gauravs/dashboard/logs/app.log

# Monitor MQTT
mosquitto_sub -h localhost -t "#" -v

# Test command
mosquitto_pub -h localhost -t "your_topic/cmnd/Power" -m "ON"
```

### Default Settings
- **MQTT Broker**: localhost:1883
- **Dashboard Port**: 80 or 5050
- **Tasmota Topic Format**: `%prefix%/%topic%/`

## 🎯 Next Steps After Verification

1. **Add More Devices**: Repeat device setup for additional ESP32s
2. **Enable Security**: Set up MQTT authentication
3. **Automation**: Use API for automated control
4. **Monitoring**: Set up device status alerts
5. **Documentation**: Read full guide for advanced features

---

**Status Key**:
- ✅ = Working correctly
- ⚠️ = Partial/needs attention
- ❌ = Not working

**Need Help?** See `docs/MQTT_TASMOTA_GUIDE.md` for detailed troubleshooting.

