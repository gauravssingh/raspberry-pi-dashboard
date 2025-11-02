"""MQTT/IoT device control routes"""
from flask import Blueprint, jsonify, request, current_app
import json
import os
from app.modules.mqtt_tasmota import get_mqtt_client, init_mqtt_client, shutdown_mqtt_client

mqtt_bp = Blueprint('mqtt', __name__)

# Path to MQTT configuration file
MQTT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'configs', 'mqtt_config.json'
)


def load_mqtt_config():
    """Load MQTT configuration from file"""
    try:
        if os.path.exists(MQTT_CONFIG_FILE):
            with open(MQTT_CONFIG_FILE, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        current_app.logger.error(f"Error loading MQTT config: {e}")
        return None


def save_mqtt_config(config):
    """Save MQTT configuration to file"""
    try:
        with open(MQTT_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        current_app.logger.error(f"Error saving MQTT config: {e}")
        return False


@mqtt_bp.route('/status', methods=['GET'])
def get_mqtt_status():
    """Get MQTT connection status"""
    try:
        client = get_mqtt_client()
        config = load_mqtt_config()
        
        if client:
            return jsonify({
                'success': True,
                'connected': client.is_connected(),
                'broker': {
                    'host': client.broker_host,
                    'port': client.broker_port
                },
                'device_count': len(client.devices)
            })
        else:
            return jsonify({
                'success': True,
                'connected': False,
                'broker': config.get('broker', {}) if config else {},
                'device_count': 0
            })
    except Exception as e:
        current_app.logger.error(f"Error getting MQTT status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/config', methods=['GET'])
def get_mqtt_config():
    """Get MQTT configuration"""
    try:
        config = load_mqtt_config()
        if config:
            # Remove password from response for security
            if 'broker' in config and 'password' in config['broker']:
                config_copy = json.loads(json.dumps(config))  # Deep copy
                config_copy['broker']['password'] = '***' if config['broker']['password'] else ''
                return jsonify({'success': True, 'config': config_copy})
            return jsonify({'success': True, 'config': config})
        return jsonify({'success': False, 'error': 'Configuration not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error getting MQTT config: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/config', methods=['POST'])
def update_mqtt_config():
    """Update MQTT configuration"""
    try:
        new_config = request.get_json()
        
        if not new_config:
            return jsonify({'success': False, 'error': 'No configuration provided'}), 400
        
        # Load existing config to preserve password if not provided
        existing_config = load_mqtt_config()
        if existing_config and 'broker' in new_config:
            if new_config['broker'].get('password') == '***':
                new_config['broker']['password'] = existing_config['broker'].get('password', '')
        
        # Save configuration
        if save_mqtt_config(new_config):
            current_app.logger.info("MQTT configuration updated")
            return jsonify({'success': True, 'message': 'Configuration updated'})
        
        return jsonify({'success': False, 'error': 'Failed to save configuration'}), 500
    except Exception as e:
        current_app.logger.error(f"Error updating MQTT config: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/connect', methods=['POST'])
def mqtt_connect():
    """Connect to MQTT broker"""
    try:
        config = load_mqtt_config()
        if not config:
            return jsonify({'success': False, 'error': 'Configuration not found'}), 404
        
        broker = config.get('broker', {})
        
        # Initialize and connect client
        client = init_mqtt_client(
            broker_host=broker.get('host', 'localhost'),
            broker_port=broker.get('port', 1883),
            username=broker.get('username') or None,
            password=broker.get('password') or None
        )
        
        if client.connect():
            # Add configured devices
            for device in config.get('devices', []):
                client.add_device(
                    name=device['name'],
                    topic=device['topic'],
                    device_type=device.get('device_type', 'generic')
                )
            
            current_app.logger.info("Connected to MQTT broker")
            return jsonify({'success': True, 'message': 'Connected to MQTT broker'})
        
        return jsonify({'success': False, 'error': 'Failed to connect to broker'}), 500
    except Exception as e:
        current_app.logger.error(f"Error connecting to MQTT broker: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/disconnect', methods=['POST'])
def mqtt_disconnect():
    """Disconnect from MQTT broker"""
    try:
        shutdown_mqtt_client()
        current_app.logger.info("Disconnected from MQTT broker")
        return jsonify({'success': True, 'message': 'Disconnected from MQTT broker'})
    except Exception as e:
        current_app.logger.error(f"Error disconnecting from MQTT broker: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/devices', methods=['GET'])
def get_devices():
    """Get list of all MQTT devices"""
    try:
        client = get_mqtt_client()
        
        if not client:
            return jsonify({'success': False, 'error': 'MQTT client not initialized'}), 400
        
        devices = client.get_devices()
        return jsonify({'success': True, 'devices': devices})
    except Exception as e:
        current_app.logger.error(f"Error getting devices: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/devices/<device_topic>', methods=['GET'])
def get_device(device_topic):
    """Get specific device status"""
    try:
        client = get_mqtt_client()
        
        if not client:
            return jsonify({'success': False, 'error': 'MQTT client not initialized'}), 400
        
        device = client.get_device(device_topic)
        
        if device:
            return jsonify({'success': True, 'device': device})
        
        return jsonify({'success': False, 'error': 'Device not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error getting device: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/devices', methods=['POST'])
def add_device():
    """Add a new device"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('topic'):
            return jsonify({'success': False, 'error': 'Name and topic required'}), 400
        
        client = get_mqtt_client()
        if not client:
            return jsonify({'success': False, 'error': 'MQTT client not initialized'}), 400
        
        # Add device to client
        device = client.add_device(
            name=data['name'],
            topic=data['topic'],
            device_type=data.get('device_type', 'generic')
        )
        
        # Update configuration file
        config = load_mqtt_config()
        if config:
            config['devices'].append({
                'name': data['name'],
                'topic': data['topic'],
                'device_type': data.get('device_type', 'generic'),
                'description': data.get('description', '')
            })
            save_mqtt_config(config)
        
        current_app.logger.info(f"Added device: {data['name']}")
        return jsonify({'success': True, 'device': device.to_dict()})
    except Exception as e:
        current_app.logger.error(f"Error adding device: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/devices/<device_topic>', methods=['DELETE'])
def remove_device(device_topic):
    """Remove a device"""
    try:
        client = get_mqtt_client()
        
        if not client:
            return jsonify({'success': False, 'error': 'MQTT client not initialized'}), 400
        
        # Remove from client
        if client.remove_device(device_topic):
            # Update configuration file
            config = load_mqtt_config()
            if config:
                config['devices'] = [d for d in config['devices'] if d['topic'] != device_topic]
                save_mqtt_config(config)
            
            current_app.logger.info(f"Removed device: {device_topic}")
            return jsonify({'success': True, 'message': 'Device removed'})
        
        return jsonify({'success': False, 'error': 'Device not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error removing device: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/command', methods=['POST'])
def send_command():
    """Send command to a device"""
    try:
        data = request.get_json()
        
        if not data or not data.get('device_topic') or not data.get('command'):
            return jsonify({'success': False, 'error': 'Device topic and command required'}), 400
        
        client = get_mqtt_client()
        
        if not client or not client.is_connected():
            return jsonify({'success': False, 'error': 'MQTT client not connected'}), 400
        
        result = client.publish_command(
            device_topic=data['device_topic'],
            command=data['command'],
            payload=data.get('payload', '')
        )
        
        if result:
            current_app.logger.info(f"Sent command to {data['device_topic']}: {data['command']}")
            return jsonify({'success': True, 'message': 'Command sent'})
        
        return jsonify({'success': False, 'error': 'Failed to send command'}), 500
    except Exception as e:
        current_app.logger.error(f"Error sending command: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/power/<device_topic>', methods=['POST'])
def control_power(device_topic):
    """Control device power (relay)"""
    try:
        data = request.get_json()
        
        if not data or 'action' not in data:
            return jsonify({'success': False, 'error': 'Action required (on/off/toggle)'}), 400
        
        client = get_mqtt_client()
        
        if not client or not client.is_connected():
            return jsonify({'success': False, 'error': 'MQTT client not connected'}), 400
        
        action = data['action'].lower()
        relay = data.get('relay')  # Optional relay number
        
        if action == 'on':
            result = client.power_on(device_topic, relay)
        elif action == 'off':
            result = client.power_off(device_topic, relay)
        elif action == 'toggle':
            result = client.power_toggle(device_topic, relay)
        else:
            return jsonify({'success': False, 'error': 'Invalid action'}), 400
        
        if result:
            current_app.logger.info(f"Power {action} for {device_topic}")
            return jsonify({'success': True, 'message': f'Power {action}'})
        
        return jsonify({'success': False, 'error': 'Failed to control power'}), 500
    except Exception as e:
        current_app.logger.error(f"Error controlling power: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/status/<device_topic>', methods=['POST'])
def request_status(device_topic):
    """Request status update from device"""
    try:
        client = get_mqtt_client()
        
        if not client or not client.is_connected():
            return jsonify({'success': False, 'error': 'MQTT client not connected'}), 400
        
        data = request.get_json() or {}
        status_type = data.get('type', 0)
        
        result = client.get_status(device_topic, status_type)
        
        if result:
            return jsonify({'success': True, 'message': 'Status request sent'})
        
        return jsonify({'success': False, 'error': 'Failed to request status'}), 500
    except Exception as e:
        current_app.logger.error(f"Error requesting status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/dimmer/<device_topic>', methods=['POST'])
def control_dimmer(device_topic):
    """Control dimmer level"""
    try:
        data = request.get_json()
        
        if not data or 'level' not in data:
            return jsonify({'success': False, 'error': 'Level required (0-100)'}), 400
        
        client = get_mqtt_client()
        
        if not client or not client.is_connected():
            return jsonify({'success': False, 'error': 'MQTT client not connected'}), 400
        
        level = int(data['level'])
        if level < 0 or level > 100:
            return jsonify({'success': False, 'error': 'Level must be between 0 and 100'}), 400
        
        result = client.set_dimmer(device_topic, level)
        
        if result:
            return jsonify({'success': True, 'message': f'Dimmer set to {level}%'})
        
        return jsonify({'success': False, 'error': 'Failed to set dimmer'}), 500
    except Exception as e:
        current_app.logger.error(f"Error controlling dimmer: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/color/<device_topic>', methods=['POST'])
def control_color(device_topic):
    """Control RGB color"""
    try:
        data = request.get_json()
        
        if not data or 'color' not in data:
            return jsonify({'success': False, 'error': 'Color required (hex format: RRGGBB)'}), 400
        
        client = get_mqtt_client()
        
        if not client or not client.is_connected():
            return jsonify({'success': False, 'error': 'MQTT client not connected'}), 400
        
        color = data['color'].replace('#', '')
        result = client.set_color(device_topic, color)
        
        if result:
            return jsonify({'success': True, 'message': f'Color set to #{color}'})
        
        return jsonify({'success': False, 'error': 'Failed to set color'}), 500
    except Exception as e:
        current_app.logger.error(f"Error controlling color: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@mqtt_bp.route('/restart/<device_topic>', methods=['POST'])
def restart_device(device_topic):
    """Restart a device"""
    try:
        client = get_mqtt_client()
        
        if not client or not client.is_connected():
            return jsonify({'success': False, 'error': 'MQTT client not connected'}), 400
        
        result = client.restart(device_topic)
        
        if result:
            return jsonify({'success': True, 'message': 'Restart command sent'})
        
        return jsonify({'success': False, 'error': 'Failed to restart device'}), 500
    except Exception as e:
        current_app.logger.error(f"Error restarting device: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

