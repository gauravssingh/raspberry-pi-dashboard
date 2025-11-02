"""Raspotify integration module - monitor and control Spotify Connect"""
import subprocess
import json
import os


def is_running():
    """Check if Raspotify service is running"""
    try:
        result = subprocess.run(
            ['/usr/bin/systemctl', 'is-active', 'raspotify'],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip() == 'active'
    except:
        return False


def get_service_status():
    """Get detailed Raspotify service status"""
    try:
        # Check if service is running
        running = is_running()
        
        # Get service info
        result = subprocess.run(
            ['/usr/bin/systemctl', 'status', 'raspotify'],
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
        
        return status_info
    except Exception as e:
        return {
            'running': False,
            'enabled': False,
            'status': 'unknown',
            'error': str(e)
        }


def get_current_track():
    """
    Get currently playing track information.
    
    Note: This requires additional setup with Spotify Web API or librespot monitoring.
    For now, this is a placeholder that can be extended later.
    
    Options for implementation:
    1. Use Spotify Web API (requires app credentials)
    2. Monitor librespot debug output
    3. Use MPRIS D-Bus interface if available
    """
    try:
        # Check if running first
        if not is_running():
            return {
                'playing': False,
                'message': 'Raspotify is not running'
            }
        
        # Placeholder - can be extended with actual implementation
        # For now, just return that service is ready
        return {
            'playing': False,
            'message': 'Raspotify is running and ready for connections',
            'note': 'Real-time track info requires Spotify Web API integration'
        }
        
        # Future implementation example:
        # If using Spotify Web API:
        # - Get current playback from https://api.spotify.com/v1/me/player
        # - Return track name, artist, album, progress, etc.
        
    except Exception as e:
        return {
            'playing': False,
            'error': str(e)
        }


def get_raspotify_config():
    """Read Raspotify configuration"""
    config_path = '/etc/raspotify/conf'
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = {}
                for line in f.readlines():
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value.strip('"').strip("'")
                return config
        return {}
    except:
        return {}


def get_device_name():
    """Get the Spotify Connect device name"""
    config = get_raspotify_config()
    return config.get('DEVICE_NAME', 'Raspotify')

