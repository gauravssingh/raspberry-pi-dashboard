#!/usr/bin/env python3
"""
Test script for GPIO module
Run this to verify GPIO setup
"""

import sys
import json
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def test_gpiod_import():
    """Test if gpiod library is available"""
    print("Testing gpiod import...")
    try:
        import gpiod
        print("✓ gpiod library imported successfully")
        print(f"  Version: {gpiod.__version__ if hasattr(gpiod, '__version__') else 'Unknown'}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import gpiod: {e}")
        print("  Install with: pip install gpiod==2.1.3")
        return False

def test_config_file():
    """Test if config file exists and is valid"""
    print("\nTesting configuration file...")
    config_path = Path(__file__).parent / 'configs' / 'gpio_config.json'
    
    if not config_path.exists():
        print(f"✗ Config file not found: {config_path}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print(f"✓ Config file loaded successfully")
        print(f"  Pins configured: {len(config.get('pins', []))}")
        
        # Show configured pins
        for pin in config.get('pins', []):
            print(f"    - {pin['name']} (GPIO {pin['gpio_number']})")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load config: {e}")
        return False

def test_gpio_module():
    """Test GPIO control module"""
    print("\nTesting GPIO control module...")
    try:
        from app.modules import gpio_control
        print("✓ GPIO control module imported successfully")
        
        # Get controller
        controller = gpio_control.get_gpio_controller()
        print(f"  Mode: {'Hardware' if gpio_control.GPIOD_AVAILABLE and controller.chip else 'Simulation'}")
        
        # Get all pins
        pins = gpio_control.get_all_pins()
        print(f"  Pins loaded: {len(pins)}")
        
        for pin in pins:
            state = "HIGH" if pin['state'] == 1 else "LOW"
            print(f"    - {pin['name']}: {state}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load GPIO module: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_routes():
    """Test if API routes are registered"""
    print("\nTesting API routes...")
    try:
        from app import create_app
        app = create_app('development')
        
        # Check if gpio blueprint is registered
        gpio_routes = [rule.rule for rule in app.url_map.iter_rules() if '/gpio' in rule.rule]
        
        if gpio_routes:
            print(f"✓ GPIO API routes registered: {len(gpio_routes)}")
            for route in sorted(gpio_routes):
                print(f"    - {route}")
            return True
        else:
            print("✗ No GPIO routes found")
            return False
            
    except Exception as e:
        print(f"✗ Failed to test API routes: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("GPIO Module Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("gpiod Import", test_gpiod_import()))
    results.append(("Config File", test_config_file()))
    results.append(("GPIO Module", test_gpio_module()))
    results.append(("API Routes", test_api_routes()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nNext steps:")
        print("1. Start the Flask app (with sudo for GPIO access)")
        print("2. Navigate to http://localhost:5050/gpio")
        print("3. Test the GPIO controls in the web interface")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

