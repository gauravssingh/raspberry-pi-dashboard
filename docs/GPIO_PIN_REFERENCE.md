# Raspberry Pi 3B - GPIO Pin Reference

## GPIO Chips Available

Based on `gpioinfo` output from your Raspberry Pi 3B:

### gpiochip0 (Main GPIO Header) - 54 lines
This is the chip we use for GPIO control. Lines 2-27 correspond to the physical GPIO header.

### gpiochip1 (System) - 2 lines
- Line 0: ACT (Activity LED)
- Line 1: Power status

### gpiochip2 (System Functions) - 8 lines
- BT_ON, WL_ON, STATUS_LED, LAN_RUN, HDMI_HPD_N, CAM_GPIO, PWR_LOW_N

## Safe GPIO Pins for Raspberry Pi 3B

### ✅ Currently Configured (Safe to Use)
| Line | Name    | Type  | Purpose in Config     |
|------|---------|-------|-----------------------|
| 17   | GPIO17  | LED   | LED 1                |
| 27   | GPIO27  | LED   | LED 2                |
| 22   | GPIO22  | Relay | Relay 1              |
| 23   | GPIO23  | Relay | Relay 2              |

### ✅ Additional Safe Pins (Available for Future Use)
| Line | Name    | Notes                          |
|------|---------|--------------------------------|
| 4    | GPIO4   | General purpose               |
| 5    | GPIO5   | General purpose               |
| 6    | GPIO6   | General purpose               |
| 12   | GPIO12  | PWM capable                   |
| 13   | GPIO13  | PWM capable                   |
| 16   | GPIO16  | General purpose               |
| 18   | GPIO18  | PWM capable                   |
| 19   | GPIO19  | SPI1 MISO (can repurpose)     |
| 20   | GPIO20  | General purpose               |
| 21   | GPIO21  | General purpose               |
| 24   | GPIO24  | General purpose               |
| 25   | GPIO25  | General purpose               |
| 26   | GPIO26  | General purpose               |

### ⚠️ PWM Capable Pins (for advanced control)
- GPIO12, GPIO13, GPIO18, GPIO40, GPIO41

### ❌ Pins to AVOID

| Lines | Name             | Reason                      |
|-------|------------------|-----------------------------|
| 0-1   | ID_SDA/ID_SCL    | HAT identification I2C     |
| 2-3   | GPIO2/GPIO3      | I2C1 (pull-up resistors)   |
| 7-11  | GPIO7-11         | SPI0 (often used)          |
| 14-15 | GPIO14/GPIO15    | UART TX/RX                 |
| 28+   | Various          | System/internal functions  |
| 44-45 | SDA0/SCL0        | Primary I2C                |

## Physical Pin Layout (GPIO Header)

```
Raspberry Pi 3B - 40 Pin GPIO Header

     3V3  (1) (2)  5V    
   GPIO2  (3) (4)  5V    
   GPIO3  (5) (6)  GND   
   GPIO4  (7) (8)  GPIO14 (UART TX)
     GND  (9) (10) GPIO15 (UART RX)
★ GPIO17 (11) (12) GPIO18 (PWM)
★ GPIO27 (13) (14) GND   
★ GPIO22 (15) (16) GPIO23 ★
     3V3 (17) (18) GPIO24
  GPIO10 (19) (20) GND   
   GPIO9 (21) (22) GPIO25
  GPIO11 (23) (24) GPIO8 
     GND (25) (26) GPIO7 
   GPIO0 (27) (28) GPIO1
   GPIO5 (29) (30) GND
   GPIO6 (31) (32) GPIO12 (PWM)
  GPIO13 (33) (34) GND
  GPIO19 (35) (36) GPIO16
  GPIO26 (37) (38) GPIO20
     GND (39) (40) GPIO21

★ = Configured in your dashboard
```

## BCM vs Physical Numbering

Your configuration uses **BCM (Broadcom) numbering**, which matches the `gpioinfo` output:

- **BCM GPIO 17** = Physical Pin 11
- **BCM GPIO 27** = Physical Pin 13
- **BCM GPIO 22** = Physical Pin 15
- **BCM GPIO 23** = Physical Pin 16

## Adding New Pins

To add more pins, edit `configs/gpio_config.json`. Safe recommendations:

### For LEDs
```json
{
  "id": "gpio_24",
  "gpio_number": 24,
  "name": "LED 3",
  "description": "Additional LED indicator",
  "type": "led",
  "direction": "output",
  "initial_state": "low",
  "group": "LEDs"
}
```

### For Buttons (Input)
```json
{
  "id": "gpio_25",
  "gpio_number": 25,
  "name": "Button 1",
  "description": "Push button input",
  "type": "button",
  "direction": "input",
  "initial_state": "low",
  "group": "Inputs"
}
```

### For PWM Devices
```json
{
  "id": "gpio_18",
  "gpio_number": 18,
  "name": "LED Dimmer",
  "description": "PWM controlled LED",
  "type": "pwm",
  "direction": "output",
  "initial_state": "low",
  "group": "PWM"
}
```

## Electrical Specifications

- **GPIO Output Voltage**: 3.3V
- **Max Current per Pin**: 16mA (recommended: 8mA)
- **Total GPIO Current**: 50mA max
- **Input High Threshold**: 1.8V
- **Input Low Threshold**: 0.8V

## Safety Notes

1. **Never connect 5V** directly to GPIO pins
2. **Always use resistors** with LEDs (220Ω - 1kΩ)
3. **Use level shifters** for 5V devices
4. **Use relays/transistors** for high current loads
5. **Add pull-up/pull-down** resistors for buttons

## Quick Reference Commands

```bash
# List all GPIO chips and lines
gpioinfo

# Get status of specific pin (GPIO 17)
gpioget gpiochip0 17

# Set pin high (requires sudo)
sudo gpioset gpiochip0 17=1

# Set pin low (requires sudo)
sudo gpioset gpiochip0 17=0

# Monitor pin changes
gpiomon gpiochip0 17
```

## Current Pin Status

When dashboard is running, pins will show as:
```
line  17: "GPIO17" output consumer="raspberry-pi-dashboard"
line  22: "GPIO22" output consumer="raspberry-pi-dashboard"
line  23: "GPIO23" output consumer="raspberry-pi-dashboard"
line  27: "GPIO27" output consumer="raspberry-pi-dashboard"
```

The `consumer` field will show "raspberry-pi-dashboard" indicating our app is controlling them.

---

**Your GPIO configuration is perfect for a Raspberry Pi 3B!** ✓

