"""GPIO API routes - REST endpoints for GPIO control"""
from flask import Blueprint, jsonify, request
from app.modules import gpio_control

gpio_bp = Blueprint('gpio', __name__)


@gpio_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'gpio'})


@gpio_bp.route('/pins')
def get_pins():
    """Get all configured GPIO pins with current states"""
    try:
        pins = gpio_control.get_all_pins()
        
        # Group pins by category
        grouped = {}
        for pin in pins:
            group = pin.get('group', 'Other')
            if group not in grouped:
                grouped[group] = []
            grouped[group].append(pin)
        
        return jsonify({
            'success': True,
            'pins': pins,
            'grouped': grouped,
            'count': len(pins)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gpio_bp.route('/pin/<pin_id>')
def get_pin(pin_id):
    """Get specific pin configuration and state"""
    try:
        pin_config = gpio_control.get_pin_config(pin_id)
        
        if not pin_config:
            return jsonify({
                'success': False,
                'error': f'Pin {pin_id} not found'
            }), 404
        
        state = gpio_control.get_pin_state(pin_id)
        
        return jsonify({
            'success': True,
            'pin': {
                **pin_config,
                'state': state
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gpio_bp.route('/pin/<pin_id>/set', methods=['POST'])
def set_pin(pin_id):
    """Set pin state to HIGH (1) or LOW (0)"""
    try:
        data = request.get_json()
        
        if not data or 'state' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "state" in request body'
            }), 400
        
        state = data['state']
        
        # Accept boolean, string, or int
        if isinstance(state, bool):
            state = 1 if state else 0
        elif isinstance(state, str):
            state = 1 if state.lower() in ['high', '1', 'on', 'true'] else 0
        elif isinstance(state, int):
            state = 1 if state > 0 else 0
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid state value'
            }), 400
        
        gpio_control.set_pin_state(pin_id, state)
        new_state = gpio_control.get_pin_state(pin_id)
        
        return jsonify({
            'success': True,
            'pin_id': pin_id,
            'state': new_state,
            'state_name': 'HIGH' if new_state == 1 else 'LOW'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gpio_bp.route('/pin/<pin_id>/toggle', methods=['POST'])
def toggle_pin(pin_id):
    """Toggle pin state (HIGH->LOW or LOW->HIGH)"""
    try:
        new_state = gpio_control.toggle_pin(pin_id)
        
        return jsonify({
            'success': True,
            'pin_id': pin_id,
            'state': new_state,
            'state_name': 'HIGH' if new_state == 1 else 'LOW'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@gpio_bp.route('/config')
def get_config():
    """Get GPIO configuration"""
    try:
        controller = gpio_control.get_gpio_controller()
        
        # Check if we have an active GPIO request (gpiod 2.x)
        hardware_mode = gpio_control.GPIOD_AVAILABLE and (controller.chip is not None and controller.request is not None)
        
        return jsonify({
            'success': True,
            'config': controller.config,
            'gpiod_available': gpio_control.GPIOD_AVAILABLE,
            'mode': 'hardware' if hardware_mode else 'simulation'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

