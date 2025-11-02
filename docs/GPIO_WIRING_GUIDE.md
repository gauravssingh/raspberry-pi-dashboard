# GPIO Wiring Guide - LED Testing with Breadboard

Complete guide for wiring LEDs to test GPIO functionality on your Raspberry Pi 3B.

---

## 🛠️ Components Needed

### Essential Components
- **Raspberry Pi 3B** (already have)
- **Breadboard** (400 or 830 tie points)
- **LEDs** x4 (any color - red, green, yellow, blue)
- **220Ω Resistors** x4 (red-red-brown or red-red-black-black-brown)
- **Jumper Wires** (Male-to-Female or Male-to-Male + Female-to-Male)

### Optional Components
- **Multimeter** (for testing continuity)
- **Different resistor values** (330Ω, 470Ω for different brightness)

---

## 📐 Breadboard Basics

### Breadboard Layout
```
    Power Rails (+ and -)
    ↓
[+ + + + + + + + + + + + + + + +]  ← Positive rail (red)
[- - - - - - - - - - - - - - - -]  ← Ground rail (blue/black)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 a b c d e | f g h i j
[○ ○ ○ ○ ○ | ○ ○ ○ ○ ○] ← Row 1
[○ ○ ○ ○ ○ | ○ ○ ○ ○ ○] ← Row 2
[○ ○ ○ ○ ○ | ○ ○ ○ ○ ○] ← Row 3
     ↑           ↑
   Connected   Not connected
   (same row)  (different rows)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[+ + + + + + + + + + + + + + + +]  ← Positive rail
[- - - - - - - - - - - - - - - -]  ← Ground rail
```

**Important:**
- Rows a-e are connected horizontally
- Rows f-j are connected horizontally
- The center gap separates the two sides
- Rails run vertically along the breadboard

---

## 🔌 GPIO Pin Reference (Raspberry Pi 3B)

### Physical Pin Layout
```
     3V3  (1) (2)  5V    
   GPIO2  (3) (4)  5V    
   GPIO3  (5) (6)  GND   ← GND (use this)
   GPIO4  (7) (8)  GPIO14
     GND  (9) (10) GPIO15 ← GND (use this)
★ GPIO17 (11) (12) GPIO18
★ GPIO27 (13) (14) GND   ← GND (use this)
★ GPIO22 (15) (16) GPIO23 ★
     3V3 (17) (18) GPIO24
  GPIO10 (19) (20) GND   ← GND (use this)
   GPIO9 (21) (22) GPIO25
  GPIO11 (23) (24) GPIO8 
     GND (25) (26) GPIO7 

★ = Configured in dashboard
```

---

## 💡 Single LED Wiring (Test Setup)

### Circuit Diagram - LED 1 (GPIO 17)

```
Raspberry Pi                  Breadboard
GPIO Header                   
                              
Pin 11 (GPIO17) ──────────────→ a1 (Breadboard)
                                 │
                              a1─┴─b1─c1 (row connected)
                                    │
                                    c1
                                    │
                              [220Ω Resistor]
                                    │
                                    c3
                                    │
                                    ├─ LED Anode (+) long leg
                                    │
                                    c5
                                    │
                                    ├─ LED Cathode (-) short leg
                                    │
                                    c7
                                    │
Pin 6 (GND) ──────────────────────┘

```

### Physical Wiring Steps

1. **Connect GND rail**
   - Jumper wire from Pi Pin 6 (GND) → Breadboard Ground rail (blue/black)

2. **Place LED**
   - Insert LED into breadboard
   - **Long leg (Anode +)** → Row 5, column c
   - **Short leg (Cathode -)** → Row 7, column c

3. **Place Resistor**
   - One leg → Row 3, column c (same column as LED)
   - Other leg → Row 1, column c

4. **Connect GPIO**
   - Jumper wire from Pi Pin 11 (GPIO17) → Row 1, column a

5. **Connect Ground**
   - Jumper wire from Row 7, column a → Ground rail

### Visual Layout
```
Breadboard (Top View):

Row  a  b  c  d  e  |  f  g  h  i  j
─────────────────────────────────────
 1  [GPIO17 wire]──[Resistor leg]
 2              
 3              [Resistor leg]
 4              
 5              [LED + (long)]
 6              
 7  [GND wire]────[LED - (short)]
 8              

Power Rails:
[+ + + + +] (not used for this)
[- - - - -] ← Connect Pi GND and LED cathode here
```

---

## 🎨 Complete 4-LED Wiring (All GPIOs)

### Full Circuit for Testing All Dashboard GPIOs

```
Components Layout on Breadboard:

         LED 1        LED 2        LED 3        LED 4
         (GPIO17)     (GPIO27)     (GPIO22)     (GPIO23)

Row  |  c  d  e  |  g  h  i  |  k  l  m  |  o  p  q
─────┼───────────┼───────────┼───────────┼──────────
  1  |  [Res] ←GPIO17  [Res] ←GPIO27  [Res] ←GPIO22  [Res] ←GPIO23
  2  |  [Res]      [Res]      [Res]      [Res]
  3  |           
  4  |  [LED+]     [LED+]     [LED+]     [LED+]
  5  |           
  6  |  [LED-]     [LED-]     [LED-]     [LED-]
  7  |    ↓          ↓          ↓          ↓
     └────────────── All to GND rail ────────────┘
```

### Wiring Table

| Component | Pi Pin | Breadboard Connection |
|-----------|--------|-----------------------|
| **LED 1 (GPIO 17)** | | |
| GPIO17 | Pin 11 | → Resistor → LED+ → LED- → GND |
| **LED 2 (GPIO 27)** | | |
| GPIO27 | Pin 13 | → Resistor → LED+ → LED- → GND |
| **LED 3 (GPIO 22)** | | |
| GPIO22 | Pin 15 | → Resistor → LED+ → LED- → GND |
| **LED 4 (GPIO 23)** | | |
| GPIO23 | Pin 16 | → Resistor → LED+ → LED- → GND |
| **Ground** | | |
| GND | Pin 6, 9, 14, or 20 | → Breadboard GND rail |

### Connection Steps

1. **Setup Ground Rail**
   ```
   Pi Pin 6 (GND) → Breadboard Ground rail (-)
   ```

2. **LED 1 - GPIO 17 (Pin 11)**
   ```
   Pi Pin 11 → Resistor (220Ω) → LED Anode (+) → LED Cathode (-) → GND rail
   ```

3. **LED 2 - GPIO 27 (Pin 13)**
   ```
   Pi Pin 13 → Resistor (220Ω) → LED Anode (+) → LED Cathode (-) → GND rail
   ```

4. **LED 3 - GPIO 22 (Pin 15)**
   ```
   Pi Pin 15 → Resistor (220Ω) → LED Anode (+) → LED Cathode (-) → GND rail
   ```

5. **LED 4 - GPIO 23 (Pin 16)**
   ```
   Pi Pin 16 → Resistor (220Ω) → LED Anode (+) → LED Cathode (-) → GND rail
   ```

---

## 🔍 LED Polarity Guide

### Identifying LED Pins

```
    Long Leg (+)
        │
        │  ┌─────┐
        └──┤     │
           │ LED │
        ┌──┤     │
        │  └─────┘
        │
    Short Leg (-)


Side View:
    Flat Edge
        │
    ┌───▼───┐
    │   -   │  ← Cathode (-)
    │ [LED] │
    │   +   │  ← Anode (+)
    └───────┘
```

**Remember:**
- **Long leg** = Anode (+) = connects to resistor
- **Short leg** = Cathode (-) = connects to GND
- **Flat edge** on LED body = Cathode (-) side

---

## ⚡ Resistor Values

### Why 220Ω?

```
Calculation:
GPIO Output: 3.3V
LED Forward Voltage: ~2.0V (red) to ~3.2V (blue)
LED Current: ~10mA (safe for Pi)

Resistor = (Vgpio - Vled) / Current
         = (3.3V - 2.0V) / 0.01A
         = 130Ω minimum

220Ω is safe and commonly available
```

### Alternative Resistor Values

| Resistor | Current | Brightness | Safety |
|----------|---------|------------|--------|
| 220Ω     | ~6mA    | Medium     | ✓ Safe |
| 330Ω     | ~4mA    | Dimmer     | ✓ Very safe |
| 470Ω     | ~3mA    | Dim        | ✓ Very safe |
| 1kΩ      | ~1.3mA  | Very dim   | ✓ Ultra safe |

**Recommendation:** Use 220Ω to 470Ω for visible but safe brightness.

---

## 🧪 Testing Procedure

### Step 1: Safety Check
Before powering on:
- [ ] All resistors in place (one per LED)
- [ ] LED polarity correct (long leg to resistor)
- [ ] No shorts between GPIO pins
- [ ] GND connections secure

### Step 2: Power On
```bash
# Start dashboard with sudo (for GPIO access)
cd /home/gauravs/dashboard
sudo venv/bin/python run.py
```

### Step 3: Test via Dashboard
1. Open browser: `http://your-pi-ip:5050/gpio`
2. Toggle LED 1 switch
3. LED should light up
4. Toggle off - LED should turn off

### Step 4: Test via API
```bash
# Turn on LED 1
curl -X POST http://localhost:5050/api/gpio/pin/gpio_17/set \
  -H "Content-Type: application/json" \
  -d '{"state": 1}'

# LED should light up

# Turn off LED 1
curl -X POST http://localhost:5050/api/gpio/pin/gpio_17/set \
  -H "Content-Type: application/json" \
  -d '{"state": 0}'

# LED should turn off
```

### Step 5: Test All LEDs
Toggle each LED one by one to verify all connections.

---

## 📷 Wiring Photos Reference

### LED + Resistor Placement
```
   Resistor (brown-black-red or red-red-brown)
   ┌─────────────┐
   │  ▬▬▬▬▬▬▬▬▬  │
───┴─────────────┴───
   │             │
   GPIO wire     LED Anode (+)


   LED
   Long leg (+) ─┐
                 │  ⚡
   Short leg (-)─┴─ → GND
```

### Complete Single LED Setup
```
Raspberry Pi GPIO Header          Breadboard
    (Side View)                   (Top View)

Pin 11 ═══════════════════════→  Row 1, Col c
(GPIO17)                           │
                                   │ [220Ω Resistor]
                                   │
                                  Row 3, Col c
                                   │
                                   │ [LED + (long leg)]
                                   │
                                  Row 5, Col c
                                   │
                                   │ [LED - (short leg)]
                                   │
Pin 6  ═══════════════════════→  Row 7, Col c → GND Rail
(GND)
```

---

## 🚨 Troubleshooting

### LED Not Lighting Up

**Check 1: Polarity**
- Swap LED 180° (reverse it)
- Long leg should go to resistor/GPIO side
- Short leg should go to GND

**Check 2: Resistor**
- Verify resistor is in circuit
- Check both legs are inserted firmly

**Check 3: Connections**
- Check jumper wires are firmly connected
- Verify GPIO pin number matches dashboard config
- Use multimeter to check continuity

**Check 4: Software**
- Check dashboard shows GPIO in "Hardware Mode" (not Simulation)
- Run with sudo: `sudo venv/bin/python run.py`
- Check GPIO state is HIGH when toggled on

### LED Always On

- GPIO might be stuck HIGH
- Check if another program is using the pin: `gpioinfo`
- Restart Pi to reset all GPIO states

### LED Very Dim

- Resistor value too high (try 220Ω instead of 1kΩ)
- Check power supply is adequate
- Try different LED (some LEDs vary in brightness)

### LED Too Bright/Hot

- Resistor value too low or missing ⚠️
- **Add resistor immediately** to prevent damage
- Use 220Ω minimum

---

## ⚡ Advanced Wiring Options

### Using Breadboard Power Rails

```
Raspberry Pi GPIO Header       Breadboard
                               
Pin 6 (GND) ════════════════→ Ground Rail (-)
                               ║
                               ║ (all cathodes connect here)
                               ║
Pin 11 (GPIO17) ═══→ [220Ω] → LED+ → LED- ═╝
Pin 13 (GPIO27) ═══→ [220Ω] → LED+ → LED- ═╝
Pin 15 (GPIO22) ═══→ [220Ω] → LED+ → LED- ═╝
Pin 16 (GPIO23) ═══→ [220Ω] → LED+ → LED- ═╝
```

### Compact 4-LED Layout

```
Breadboard Compact Layout:

         GND Rail
           ║
    ┌──────╨──────┐
    │   - - - -   │
    └─────────────┘
    
    LED1  LED2  LED3  LED4
     │     │     │     │
    [R]   [R]   [R]   [R]
     │     │     │     │
    Pin11 Pin13 Pin15 Pin16
    GP17  GP27  GP22  GP23

R = 220Ω Resistor
```

---

## 🎯 Quick Test Commands

### Dashboard Web Interface
```
http://your-pi-ip:5050/gpio
```

### Command Line Tests

```bash
# Test GPIO 17 (LED 1)
sudo gpioset gpiochip0 17=1    # Turn ON
sleep 2
sudo gpioset gpiochip0 17=0    # Turn OFF

# Test GPIO 27 (LED 2)
sudo gpioset gpiochip0 27=1    # Turn ON
sleep 2
sudo gpioset gpiochip0 27=0    # Turn OFF
```

### API Tests

```bash
# Automated test script
for pin in gpio_17 gpio_27 gpio_22 gpio_23; do
  echo "Testing $pin..."
  
  # Turn ON
  curl -X POST http://localhost:5050/api/gpio/pin/$pin/set \
    -H "Content-Type: application/json" -d '{"state": 1}'
  sleep 2
  
  # Turn OFF
  curl -X POST http://localhost:5050/api/gpio/pin/$pin/set \
    -H "Content-Type: application/json" -d '{"state": 0}'
  sleep 1
done
```

---

## 🛡️ Safety Guidelines

### Before Connecting
- ✅ **Always** use resistors with LEDs (220Ω minimum)
- ✅ **Double-check** polarity before powering on
- ✅ **Verify** no shorts between GPIO pins
- ✅ **Power off** Pi before making changes

### During Operation
- ✅ **Monitor** LED temperature (should be cool/warm, not hot)
- ✅ **Check** GPIO doesn't exceed 16mA per pin
- ✅ **Use** multimeter to verify voltages if unsure

### Never Do This
- ❌ **Never** connect LED directly without resistor
- ❌ **Never** exceed 3.3V on GPIO pins
- ❌ **Never** draw more than 16mA from a GPIO pin
- ❌ **Never** connect 5V to GPIO pins
- ❌ **Never** short GPIO to GND

---

## 📊 Expected Behavior

### When Working Correctly

| Dashboard Action | LED Behavior | GPIO Voltage |
|------------------|--------------|--------------|
| Toggle ON        | LED lights up | 3.3V        |
| Toggle OFF       | LED turns off | 0V          |
| Status: HIGH     | LED on       | 3.3V        |
| Status: LOW      | LED off      | 0V          |

### Verification Commands

```bash
# Check if GPIO is claimed by dashboard
gpioinfo gpiochip0 | grep -A1 "line  17"

# Should show:
# line  17: "GPIO17" output consumer="raspberry-pi-dashboard"

# Read GPIO state
gpioget gpiochip0 17

# Returns: 0 (LOW) or 1 (HIGH)
```

---

## 🔄 Testing Pattern

### Automated Blink Test

Create this test script:

```bash
#!/bin/bash
# test_leds.sh

echo "Testing all 4 LEDs..."

for i in {1..3}; do
  echo "Cycle $i of 3"
  
  # Turn all ON
  for pin in gpio_17 gpio_27 gpio_22 gpio_23; do
    curl -s -X POST http://localhost:5050/api/gpio/pin/$pin/set \
      -H "Content-Type: application/json" -d '{"state": 1}' > /dev/null
  done
  echo "  All LEDs ON"
  sleep 2
  
  # Turn all OFF
  for pin in gpio_17 gpio_27 gpio_22 gpio_23; do
    curl -s -X POST http://localhost:5050/api/gpio/pin/$pin/set \
      -H "Content-Type: application/json" -d '{"state": 0}' > /dev/null
  done
  echo "  All LEDs OFF"
  sleep 1
done

echo "Test complete!"
```

Run with:
```bash
chmod +x test_leds.sh
./test_leds.sh
```

---

## 📸 Wiring Checklist

Before testing, verify:

- [ ] Breadboard has power rails connected to Pi GND
- [ ] Each LED has correct polarity (long leg = +)
- [ ] Each LED has 220Ω resistor in series
- [ ] GPIO wires connected to correct pins (11, 13, 15, 16)
- [ ] No loose connections or shorts
- [ ] Dashboard running with sudo for GPIO access
- [ ] All 4 pins showing in dashboard GPIO page

---

## 🎓 Learning Resources

### Understanding GPIO
- Max voltage: 3.3V
- Max current per pin: 16mA
- Total GPIO current: 50mA max
- BCM numbering (not physical pin numbers)

### LED Specifications
- Forward voltage: 1.8V-3.2V (depends on color)
- Forward current: 10-20mA typical
- Red/Yellow: ~2.0V
- Green: ~2.2V
- Blue/White: ~3.2V

### Current Calculation
```
I = (Vgpio - Vled) / R
I = (3.3V - 2.0V) / 220Ω
I = 5.9mA ✓ Safe!
```

---

## 🔗 Quick Links

- **Dashboard GPIO Page**: http://your-pi-ip:5050/gpio
- **GPIO API Docs**: [GPIO.md](GPIO.md)
- **Pin Reference**: [GPIO_PIN_REFERENCE.md](GPIO_PIN_REFERENCE.md)
- **Raspberry Pi Pinout**: https://pinout.xyz/

---

## 📝 Shopping List

If you need to purchase components:

**Essential:**
- [ ] Breadboard (400 or 830 points) - ~$3-5
- [ ] LEDs assorted pack (100+ LEDs) - ~$5
- [ ] Resistor kit (220Ω, 330Ω, 470Ω) - ~$5
- [ ] Jumper wire kit (M-M, M-F, F-F) - ~$5

**Optional:**
- [ ] Multimeter (for testing) - ~$10-15
- [ ] GPIO breakout board - ~$5
- [ ] Breadboard power supply - ~$5

**Total:** ~$15-20 for complete setup

---

## ✅ Success Checklist

After wiring and testing:

- [x] All LEDs light up when toggled ON via dashboard
- [x] All LEDs turn off when toggled OFF
- [x] No LEDs are hot to touch
- [x] Dashboard shows correct GPIO states
- [x] API commands work correctly
- [x] No error messages in logs
- [x] GPIO page shows "Hardware Mode" (not simulation)

---

**Happy wiring! Your Raspberry Pi GPIO testing setup is ready!** 🎉

---

*Last updated: November 2, 2025*
*For Raspberry Pi 3B with dashboard configured GPIOs: 17, 27, 22, 23*

