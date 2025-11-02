"""System information module - gets system-wide configuration"""
import socket
import logging

logger = logging.getLogger(__name__)


def get_local_ip():
    """Get the local IP address of the Raspberry Pi"""
    try:
        # Try to get IP from hostname
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # If we got localhost, try another method
        if local_ip.startswith('127.'):
            # Create a socket to determine the default route IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # Doesn't need to be reachable
                s.connect(('8.8.8.8', 80))
                local_ip = s.getsockname()[0]
            except Exception:
                local_ip = '127.0.0.1'
            finally:
                s.close()
        
        logger.info(f"Local IP address detected: {local_ip}")
        return local_ip
    except Exception as e:
        logger.error(f"Error getting local IP: {e}", exc_info=True)
        return '127.0.0.1'


def get_hostname():
    """Get the hostname of the Raspberry Pi"""
    try:
        return socket.gethostname()
    except Exception as e:
        logger.error(f"Error getting hostname: {e}", exc_info=True)
        return 'raspberrypi'


def get_fqdn():
    """Get the fully qualified domain name"""
    try:
        return socket.getfqdn()
    except Exception as e:
        logger.error(f"Error getting FQDN: {e}", exc_info=True)
        return 'raspberrypi.local'


# Cache the IP address at module load time
_cached_local_ip = None
_cached_hostname = None


def get_system_config():
    """Get system configuration including IP and hostname"""
    global _cached_local_ip, _cached_hostname
    
    if _cached_local_ip is None:
        _cached_local_ip = get_local_ip()
    
    if _cached_hostname is None:
        _cached_hostname = get_hostname()
    
    return {
        'local_ip': _cached_local_ip,
        'hostname': _cached_hostname,
        'fqdn': get_fqdn()
    }


# Get system config on module import
SYSTEM_CONFIG = get_system_config()
LOCAL_IP = SYSTEM_CONFIG['local_ip']
HOSTNAME = SYSTEM_CONFIG['hostname']

