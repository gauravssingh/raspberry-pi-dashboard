# Configuration Files

This directory contains JSON configuration files for the dashboard.

## Files

- **`gpio_config.json`** - GPIO pin configuration
  - Defines GPIO pins, their types, initial states, and grouping
  - See [GPIO.md](../docs/GPIO.md) for configuration details

- **`system_config.json`** - System network configuration
  - Network settings (IP, hostname)
  - System information
  - Auto-detected at runtime if not specified

## Adding New Configuration Files

When adding new JSON config files:

1. Place them in this `configs/` directory
2. Update the code to reference them with the `configs/` prefix
3. Document them in the appropriate documentation file
4. Add them to `.gitignore` if they contain sensitive information

## Example Structure

```json
{
  "pins": [
    {
      "id": "gpio_17",
      "gpio_number": 17,
      "name": "LED 1",
      "type": "led",
      "direction": "output",
      "initial_state": "low",
      "group": "LEDs"
    }
  ],
  "settings": {
    "chip": "gpiochip0",
    "consumer": "raspberry-pi-dashboard"
  }
}
```

## Notes

- Configuration files are loaded dynamically
- Changes to config files may require a page reload (not a server restart)
- Always validate JSON syntax before saving
- Keep backups of working configurations

