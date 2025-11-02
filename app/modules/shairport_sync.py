"""Shairport Sync integration module - monitor and control AirPlay Audio Receiver"""
import subprocess
import os


def is_running():
    """Check if Shairport Sync service is running"""
    try:
        result = subprocess.run(
            ['/usr/bin/systemctl', 'is-active', 'shairport-sync'],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip() == 'active'
    except:
        return False


def get_service_status():
    """Get detailed Shairport Sync service status"""
    try:
        # Check if service is running
        running = is_running()
        
        # Get service info
        result = subprocess.run(
            ['/usr/bin/systemctl', 'status', 'shairport-sync'],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        # Parse output for additional info
        lines = result.stdout.split('\n')
        status_info = {
            'running': running,
            'enabled': 'enabled' in result.stdout.lower(),
            'status': 'active' if running else 'inactive'
        }
        
        # Try to get PID if running
        if running:
            for line in lines:
                if 'Main PID:' in line:
                    try:
                        pid = line.split('Main PID:')[1].strip().split()[0]
                        status_info['pid'] = pid
                    except:
                        pass
        
        return status_info
    except Exception as e:
        return {
            'running': False,
            'enabled': False,
            'status': 'unknown',
            'error': str(e)
        }


def get_current_playback():
    """
    Get current playback information.
    
    Note: Shairport Sync doesn't expose real-time playback info easily.
    This is a placeholder that can be extended with metadata pipe monitoring.
    
    Options for implementation:
    1. Monitor metadata pipe (/tmp/shairport-sync-metadata)
    2. Use MQTT if configured
    3. Parse log output (not recommended)
    """
    try:
        # Check if running first
        if not is_running():
            return {
                'playing': False,
                'message': 'Shairport Sync is not running'
            }
        
        # Check if metadata pipe exists
        metadata_pipe = '/tmp/shairport-sync-metadata'
        if os.path.exists(metadata_pipe):
            return {
                'playing': False,
                'message': 'Shairport Sync is running and ready for AirPlay connections',
                'metadata_available': True,
                'note': 'Real-time playback info requires metadata pipe monitoring'
            }
        
        # Placeholder - service is ready
        return {
            'playing': False,
            'message': 'Shairport Sync is running and ready for AirPlay connections',
            'metadata_available': False,
            'note': 'Enable metadata pipe in config for playback info'
        }
        
    except Exception as e:
        return {
            'playing': False,
            'error': str(e)
        }


def get_shairport_config():
    """Read Shairport Sync configuration"""
    config_path = '/etc/shairport-sync.conf'
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_content = f.read()
                return {
                    'config_exists': True,
                    'config_path': config_path
                }
        return {'config_exists': False}
    except:
        return {'config_exists': False, 'error': 'Cannot read config'}


def get_device_name():
    """
    Get the AirPlay device name.
    
    Shairport Sync typically uses the hostname as the device name,
    unless configured differently in the config file.
    """
    try:
        # Try to get from config first
        config_path = '/etc/shairport-sync.conf'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('name =') or line.startswith('name='):
                        # Extract name from: name = "Device Name";
                        # Split by '=' and take the part after it
                        value = line.split('=', 1)[1].strip()
                        # Remove quotes, semicolons, and comments
                        if '//' in value:
                            value = value.split('//')[0].strip()
                        value = value.rstrip(';').strip().strip('"').strip("'")
                        if value:
                            # Handle %h placeholder (hostname)
                            if '%h' in value:
                                import socket
                                hostname = socket.gethostname()
                                value = value.replace('%h', hostname)
                            return value
        
        # Fallback to hostname
        import socket
        return socket.gethostname()
    except:
        return 'Shairport Sync'

