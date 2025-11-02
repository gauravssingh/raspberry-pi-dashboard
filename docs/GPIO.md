# GPIO Control Guide

Complete guide for setting up and using GPIO control on your Raspberry Pi dashboard.

---

## 🚀 Quick Start

### 1. Installation

The GPIO control module uses `libgpiod` Python bindings. Install it with:

```bash
# Activate your virtual environment
cd /home/gauravs/dashboard
source venv/bin/activate

# Install gpiod
pip install gpiod==2.1.3
```

**Note**: If you encounter issues, install the system library first:
```bash
sudo apt-get update
sudo apt-get install -y libgpiod-dev python3-libgpiod gpiod
```

### 2. Verify Installation

Test that gpiod is installed correctly:
```bash
python3 -c "import gpiod; print('gpiod installed successfully')"
```

### 3. Start the Dashboard (with GPIO access)

GPIO control requires root permissions:

```bash
cd /home/gauravs/dashboard
sudo venv/bin/python run.py
```

**Alternative**: Configure udev rules for non-root access (see [Permissions](#permissions) section below).

### 4. Access GPIO Control

Open your browser and navigate to:
```
http://your-pi-ip:5000/gpio
```

### 5. Control Your GPIO Pins

- **Toggle switches** - Turn pins ON/OFF
- **Status indicators** - Green (HIGH) / Gray (LOW)
- **Auto-refresh** - Updates every 5 seconds

---

## 📋 Default Configuration

Your dashboard is pre-configured with 4 GPIO pins:

| Pin Name | GPIO # | Type  | Purpose                |
|----------|--------|-------|------------------------|
| LED 1    | 17     | LED   | Primary LED indicator  |
| LED 2    | 27     | LED   | Secondary LED indicator|
| Relay 1  | 22     | Relay | Primary relay control  |
| Relay 2  | 23     | Relay | Secondary relay control|

---

## ⚙️ Configuration

### GPIO Pin Configuration

Edit `configs/gpio_config.json` to configure your GPIO pins:

```json
{
  "pins": [
    {
      "id": "gpio_17",
      "gpio_number": 17,
      "name": "LED 1",
      "description": "Primary LED indicator",
      "type": "led",
      "direction": "output",
      "initial_state": "low",
      "group": "LEDs"
    }
  ],
  "settings": {
    "chip": "gpiochip0",
    "consumer": "raspberry-pi-dashboard",
    "description": "Raspberry Pi 3B - gpiochip0 (54 lines available)"
  }
}
```

### Configuration Parameters

- **id**: Unique identifier for the pin (used in API calls)
- **gpio_number**: BCM GPIO number (17, 27, 22, etc.)
- **name**: Display name in UI
- **description**: Brief description of purpose
- **type**: Pin type (`led`, `relay`, `sensor`, etc.)
- **direction**: `output` or `input`
- **initial_state**: `low` (0V) or `high` (3.3V)
- **group**: Group name for UI organization

### Adding More Pins

1. Edit `configs/gpio_config.json`
2. Add new pin configuration
3. Reload the web page (no restart needed)
4. Configuration will be loaded dynamically

Example - Add a fan control:
```json
{
  "id": "gpio_24",
  "gpio_number": 24,
  "name": "Cooling Fan",
  "description": "Case cooling fan",
  "type": "fan",
  "direction": "output",
  "initial_state": "low",
  "group": "Cooling"
}
```

For more pin options and pin reference, see [GPIO_PIN_REFERENCE.md](GPIO_PIN_REFERENCE.md).

---

## 🔌 Hardware Connections

### LED Connection
```
GPIO Pin -> 220Ω Resistor -> LED Anode (+) -> LED Cathode (-) -> GND
```

**📐 For detailed breadboard wiring diagrams, see [GPIO_WIRING_GUIDE.md](GPIO_WIRING_GUIDE.md)**

### Relay Connection
```
GPIO Pin -> Relay Signal Pin
VCC -> 3.3V or 5V (check relay specs)
GND -> Ground
```

**⚠️ Important:**
- Always use current-limiting resistors with LEDs (220Ω recommended)
- Pi GPIO pins output 3.3V, max 16mA per pin
- For high-power devices, always use relays or transistors
- Never connect loads directly to GPIO pins

**Need help wiring?** See the [GPIO Wiring Guide](GPIO_WIRING_GUIDE.md) for step-by-step breadboard instructions with diagrams.

---

## 🌐 REST API

### Get All Pins
```bash
curl http://localhost:5000/api/gpio/pins
```

### Get Specific Pin
```bash
curl http://localhost:5000/api/gpio/pin/gpio_17
```

### Set Pin State
```bash
# Set HIGH
curl -X POST http://localhost:5000/api/gpio/pin/gpio_17/set \
  -H "Content-Type: application/json" \
  -d '{"state": 1}'

# Set LOW
curl -X POST http://localhost:5000/api/gpio/pin/gpio_17/set \
  -H "Content-Type: application/json" \
  -d '{"state": 0}'
```

### Toggle Pin
```bash
curl -X POST http://localhost:5000/api/gpio/pin/gpio_17/toggle
```

### Get Configuration
```bash
curl http://localhost:5000/api/gpio/config
```

For complete API documentation, see [API.md](API.md#gpio-endpoints).

---

## 🔐 Permissions

### Option A: Run Flask app as root (Quick Setup)
```bash
sudo /home/gauravs/dashboard/venv/bin/python /home/gauravs/dashboard/run.py
```

### Option B: Configure udev rules (Recommended for Production)

Create udev rules to allow non-root access:

```bash
# Create udev rule file
sudo nano /etc/udev/rules.d/99-gpio.rules
```

Add this content:
```
SUBSYSTEM=="gpio", KERNEL=="gpiochip*", MODE="0660", GROUP="gpio"
```

Create gpio group and add your user:
```bash
sudo groupadd -f gpio
sudo usermod -a -G gpio $USER
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Reboot for changes to take effect:
```bash
sudo reboot
```

---

## 🛠️ Troubleshooting

### 1. "gpiod not available" Error
- Install libgpiod: `sudo apt-get install libgpiod-dev python3-libgpiod`
- Install Python package: `pip install gpiod`
- System will run in simulation mode if gpiod is unavailable

### 2. Permission Denied
- Run as root or configure udev rules (see [Permissions](#permissions) section)
- Check user is in gpio group: `groups $USER`

### 3. Pin Already in Use
- Another process is using the GPIO pin
- Check running processes: `sudo lsof /dev/gpiochip0`
- Restart Pi to release all GPIO pins

### 4. Pin Not Responding
- Verify wiring and connections
- Check pin number in config (BCM numbering)
- Test with command line: `gpioget gpiochip0 17`

### 5. "Simulation Mode" shown?
Run Flask with sudo: `sudo venv/bin/python run.py`

### 6. Pin Not Found
- Verify GPIO number in `configs/gpio_config.json` uses BCM numbering
- Check pin is available: `gpioinfo gpiochip0`
- See [GPIO_PIN_REFERENCE.md](GPIO_PIN_REFERENCE.md) for safe pins

---

## 🧪 Development Mode

If gpiod is not available, the module runs in **simulation mode**:
- All API calls work normally
- Pin states are simulated in memory
- UI shows "Simulation Mode" indicator
- Great for testing without hardware

---

## ⚡ Features

✅ **Dynamic Configuration** - Add/remove pins via JSON config  
✅ **Grouped UI** - Pins organized by function  
✅ **Real-time Updates** - Auto-refresh every 5 seconds  
✅ **Status Indicators** - Visual LED indicators for pin states  
✅ **REST API** - Full API for automation and integration  
✅ **Simulation Mode** - Test without hardware  
✅ **Extensible** - Easy to add new pin types and controls  

---

## 🛡️ Safety Notes

⚠️ **Always follow these safety guidelines:**

1. Never exceed GPIO voltage ratings (3.3V max)
2. Never draw more than 16mA from a GPIO pin
3. Always use appropriate resistors and protection circuits
4. Double-check wiring before powering on
5. Use optocouplers for isolation when controlling AC devices
6. Never hot-swap GPIO connections

---

## 📚 Related Documentation

- **[GPIO_PIN_REFERENCE.md](GPIO_PIN_REFERENCE.md)** - Complete pin reference and hardware details
- **[GPIO_IMPLEMENTATION.md](GPIO_IMPLEMENTATION.md)** - Technical implementation details
- **[API.md](API.md)** - Complete API reference
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - General dashboard setup

---

## 🧪 Testing

Run the test suite to verify installation:
```bash
python test_gpio.py
```

Tests verify:
- ✓ gpiod library installed
- ✓ Configuration file valid
- ✓ GPIO module loads
- ✓ API routes registered

---

## 🆘 Support

For issues or questions:
- Check documentation: `/docs` page
- Review logs: `/logs` page
- Test API: `/api/gpio/health`
- Check [GPIO_PIN_REFERENCE.md](GPIO_PIN_REFERENCE.md) for pin details

---

**Ready to control your Raspberry Pi GPIO pins! 🎉**

