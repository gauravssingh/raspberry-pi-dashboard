"""GPIO control module - manages GPIO pins via libgpiod"""
import json
import os
import logging
from pathlib import Path

# Get logger for this module
logger = logging.getLogger(__name__)

# Try to import gpiod, but don't fail if not available (for development)
try:
    import gpiod
    from gpiod.line import Direction, Value
    GPIOD_AVAILABLE = True
except ImportError:
    GPIOD_AVAILABLE = False
    logger.warning("gpiod not available. GPIO functions will be simulated.")


class GPIOController:
    """Manages GPIO pins using libgpiod 2.x"""
    
    def __init__(self, config_path='configs/gpio_config.json'):
        """Initialize GPIO controller with config file"""
        self.config_path = config_path
        self.config = self._load_config()
        self.chip = None
        self.request = None
        self.pin_offsets = {}  # Map pin_id to GPIO number
        
        if GPIOD_AVAILABLE:
            self._initialize_gpio()
        else:
            # Simulation mode for development
            self.simulated_states = {}
            for pin in self.config['pins']:
                pin_id = pin['id']
                self.simulated_states[pin_id] = 0 if pin['initial_state'] == 'low' else 1
    
    def _load_config(self):
        """Load GPIO configuration from JSON file"""
        # Look for config in configs directory
        config_file = Path(__file__).parent.parent.parent / self.config_path
        
        if not config_file.exists():
            raise FileNotFoundError(f"GPIO config file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def _initialize_gpio(self):
        """Initialize GPIO chip and lines using gpiod 2.x API"""
        if not GPIOD_AVAILABLE:
            return
        
        try:
            chip_name = self.config['settings'].get('chip', 'gpiochip0')
            consumer_name = self.config['settings'].get('consumer', 'pi-dashboard')
            
            # Open GPIO chip with full path
            chip_path = f'/dev/{chip_name}' if not chip_name.startswith('/') else chip_name
            logger.info(f"Opening GPIO chip: {chip_path}")
            self.chip = gpiod.Chip(chip_path)
            
            # Build line configuration for gpiod 2.x
            line_config = {}
            
            for pin in self.config['pins']:
                if pin['direction'] == 'output':
                    gpio_num = pin['gpio_number']
                    pin_id = pin['id']
                    
                    # Store mapping
                    self.pin_offsets[pin_id] = gpio_num
                    
                    # Set initial value
                    initial_value = Value.INACTIVE if pin['initial_state'] == 'low' else Value.ACTIVE
                    
                    # Create line settings for this pin
                    line_config[gpio_num] = gpiod.LineSettings(
                        direction=Direction.OUTPUT,
                        output_value=initial_value
                    )
            
            # Request all lines at once
            if line_config:
                self.request = self.chip.request_lines(
                    consumer=consumer_name,
                    config=line_config
                )
                logger.info(f"GPIO initialized successfully in hardware mode. Pins: {list(self.pin_offsets.keys())}")
            
        except Exception as e:
            logger.error(f"Error initializing GPIO: {e}", exc_info=True)
            # Fall back to simulation mode
            self.chip = None
            self.request = None
            self.simulated_states = {}
            for pin in self.config['pins']:
                pin_id = pin['id']
                self.simulated_states[pin_id] = 0 if pin['initial_state'] == 'low' else 1
    
    def get_all_pins(self):
        """Get configuration for all pins"""
        pins_with_state = []
        
        for pin in self.config['pins']:
            pin_id = pin['id']
            state = self.get_pin_state(pin_id)
            
            pins_with_state.append({
                **pin,
                'state': state
            })
        
        return pins_with_state
    
    def get_pin_config(self, pin_id):
        """Get configuration for a specific pin"""
        for pin in self.config['pins']:
            if pin['id'] == pin_id:
                return pin
        return None
    
    def get_pin_state(self, pin_id):
        """Get current state of a pin (0=LOW, 1=HIGH)"""
        if not GPIOD_AVAILABLE or self.request is None:
            # Simulation mode
            return self.simulated_states.get(pin_id, 0)
        
        try:
            if pin_id in self.pin_offsets:
                gpio_num = self.pin_offsets[pin_id]
                value = self.request.get_value(gpio_num)
                return 1 if value == Value.ACTIVE else 0
            return 0
        except Exception as e:
            logger.error(f"Error reading pin {pin_id}: {e}", exc_info=True)
            return 0
    
    def set_pin_state(self, pin_id, state):
        """Set pin state (0=LOW, 1=HIGH)"""
        pin_config = self.get_pin_config(pin_id)
        
        if not pin_config:
            raise ValueError(f"Pin {pin_id} not found in configuration")
        
        if pin_config['direction'] != 'output':
            raise ValueError(f"Pin {pin_id} is not configured as output")
        
        # Validate state
        if state not in [0, 1]:
            raise ValueError("State must be 0 (LOW) or 1 (HIGH)")
        
        if not GPIOD_AVAILABLE or self.request is None:
            # Simulation mode
            self.simulated_states[pin_id] = state
            logger.debug(f"[SIMULATION] Set {pin_id} (GPIO {pin_config['gpio_number']}) to {state}")
            return True
        
        try:
            if pin_id in self.pin_offsets:
                gpio_num = self.pin_offsets[pin_id]
                value = Value.ACTIVE if state == 1 else Value.INACTIVE
                self.request.set_value(gpio_num, value)
                logger.info(f"Set {pin_id} (GPIO {gpio_num}) to {'HIGH' if state == 1 else 'LOW'}")
                return True
            else:
                raise ValueError(f"Pin {pin_id} not initialized")
        except Exception as e:
            logger.error(f"Error setting pin {pin_id}: {e}", exc_info=True)
            raise
    
    def toggle_pin(self, pin_id):
        """Toggle pin state"""
        current_state = self.get_pin_state(pin_id)
        new_state = 1 if current_state == 0 else 0
        self.set_pin_state(pin_id, new_state)
        return new_state
    
    def cleanup(self):
        """Release GPIO resources"""
        if GPIOD_AVAILABLE and self.request:
            try:
                self.request.release()
                logger.info("GPIO resources released")
            except Exception as e:
                logger.error(f"Error during GPIO cleanup: {e}", exc_info=True)
        
        if GPIOD_AVAILABLE and self.chip:
            try:
                self.chip.close()
            except Exception as e:
                logger.error(f"Error closing GPIO chip: {e}", exc_info=True)
    
    def __del__(self):
        """Cleanup on destruction"""
        self.cleanup()


# Global controller instance
_gpio_controller = None


def get_gpio_controller():
    """Get or create global GPIO controller instance"""
    global _gpio_controller
    if _gpio_controller is None:
        _gpio_controller = GPIOController()
    return _gpio_controller


def get_all_pins():
    """Get all configured pins with current states"""
    controller = get_gpio_controller()
    return controller.get_all_pins()


def get_pin_state(pin_id):
    """Get state of specific pin"""
    controller = get_gpio_controller()
    return controller.get_pin_state(pin_id)


def set_pin_state(pin_id, state):
    """Set state of specific pin"""
    controller = get_gpio_controller()
    return controller.set_pin_state(pin_id, state)


def toggle_pin(pin_id):
    """Toggle pin state"""
    controller = get_gpio_controller()
    return controller.toggle_pin(pin_id)


def get_pin_config(pin_id):
    """Get configuration for specific pin"""
    controller = get_gpio_controller()
    return controller.get_pin_config(pin_id)
