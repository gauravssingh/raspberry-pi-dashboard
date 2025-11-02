"""System monitoring module - collects Raspberry Pi system statistics"""
import psutil
import os
import subprocess
import platform
import socket
import logging
from datetime import datetime
import requests

# Get logger for this module
logger = logging.getLogger(__name__)


def get_cpu_temp():
    """Get CPU temperature"""
    try:
        temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        return float(temp.replace('temp=', '').replace("'C\n", ''))
    except:
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                return float(f.read()) / 1000.0
        except:
            return None


def get_uptime():
    """Get system uptime"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = int(float(f.read().split()[0]))
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        return {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': uptime_seconds
        }
    except Exception as e:
        logger.error(f"Error getting uptime: {e}", exc_info=True)
        return None


def get_pi_model():
    """Get Raspberry Pi model"""
    try:
        with open('/proc/device-tree/model', 'r') as f:
            return f.read().strip().replace('\x00', '')
    except:
        return platform.machine()


def get_os_info():
    """Get OS information"""
    try:
        with open('/etc/os-release', 'r') as f:
            lines = f.readlines()
            os_info = {}
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os_info[key] = value.strip('"')
            return os_info.get('PRETTY_NAME', 'Unknown')
    except:
        return platform.platform()


def get_cpu_per_core():
    """Get CPU usage per core"""
    return psutil.cpu_percent(interval=0, percpu=True)


def get_throttle_status():
    """Get Pi throttle status"""
    try:
        throttle = subprocess.check_output(['vcgencmd', 'get_throttled']).decode()
        value = int(throttle.split('=')[1], 16)
        
        status = {
            'under_voltage': bool(value & 0x1),
            'freq_capped': bool(value & 0x2),
            'throttled': bool(value & 0x4),
            'soft_temp_limit': bool(value & 0x8),
            'under_voltage_occurred': bool(value & 0x10000),
            'freq_capped_occurred': bool(value & 0x20000),
            'throttled_occurred': bool(value & 0x40000),
            'soft_temp_limit_occurred': bool(value & 0x80000)
        }
        return status
    except:
        return None


def get_top_processes():
    """Get top memory consuming processes"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'memory_percent': round(proc.info['memory_percent'], 2)
            })
        except:
            pass
    return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]


def get_partitions():
    """Get partition usage"""
    partitions = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': round(usage.total / (1024**3), 2),
                'used': round(usage.used / (1024**3), 2),
                'free': round(usage.free / (1024**3), 2),
                'percent': round(usage.percent, 1)
            })
        except:
            pass
    return partitions


def get_network_interfaces():
    """Get network interface status"""
    interfaces = {}
    try:
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        for interface, addr_list in addrs.items():
            if interface in stats:
                ip_addresses = [addr.address for addr in addr_list if addr.family == socket.AF_INET]
                interfaces[interface] = {
                    'ip': ip_addresses[0] if ip_addresses else None,
                    'is_up': stats[interface].isup,
                    'speed': stats[interface].speed
                }
    except:
        pass
    return interfaces


def get_wifi_signal():
    """Get WiFi signal strength"""
    try:
        result = subprocess.check_output(['/usr/sbin/iwconfig', 'wlan0'], stderr=subprocess.DEVNULL).decode()
        for line in result.split('\n'):
            if 'Signal level' in line:
                signal = line.split('Signal level=')[1].split(' ')[0]
                return signal
    except:
        return None


def get_wifi_details():
    """Get detailed WiFi information including SSID, frequency, and band"""
    wifi_info = {
        'ssid': None,
        'frequency': None,
        'band': None,
        'signal_strength': None,
        'signal_quality': None,
        'bit_rate': None,
        'tx_power': None,
        'link_quality': None
    }
    
    try:
        # Get info from iwconfig
        iwconfig_result = subprocess.check_output(['/usr/sbin/iwconfig', 'wlan0'], stderr=subprocess.DEVNULL).decode()
        
        for line in iwconfig_result.split('\n'):
            # Extract SSID
            if 'ESSID:' in line:
                ssid = line.split('ESSID:')[1].strip().strip('"')
                wifi_info['ssid'] = ssid if ssid else None
            
            # Extract frequency and calculate band
            if 'Frequency:' in line:
                freq_str = line.split('Frequency:')[1].split(' ')[0]
                try:
                    frequency = float(freq_str)
                    wifi_info['frequency'] = f"{frequency} GHz"
                    
                    # Determine band based on frequency
                    if 2.4 <= frequency < 2.5:
                        wifi_info['band'] = '2.4 GHz'
                    elif 5.0 <= frequency < 6.0:
                        wifi_info['band'] = '5 GHz'
                    elif frequency >= 6.0:
                        wifi_info['band'] = '6 GHz (WiFi 6E)'
                except:
                    pass
            
            # Extract signal strength
            if 'Signal level=' in line:
                try:
                    # Get the signal level portion
                    signal_part = line.split('Signal level=')[1]
                    # Extract the value with dBm
                    signal = signal_part.split()[0] + ' ' + signal_part.split()[1] if 'dBm' in signal_part else signal_part.split()[0]
                    wifi_info['signal_strength'] = signal
                    
                    # Calculate signal quality percentage (assuming -100 to -50 dBm range)
                    if 'dBm' in signal:
                        dbm = int(signal.split()[0])
                        quality = min(100, max(0, 2 * (dbm + 100)))
                        wifi_info['signal_quality'] = f"{quality}%"
                except Exception as e:
                    pass
            
            # Extract link quality
            if 'Link Quality=' in line:
                try:
                    link_quality = line.split('Link Quality=')[1].split(' ')[0]
                    wifi_info['link_quality'] = link_quality
                except:
                    pass
            
            # Extract bit rate
            if 'Bit Rate=' in line:
                try:
                    bit_rate_parts = line.split('Bit Rate=')[1].split()
                    wifi_info['bit_rate'] = ' '.join(bit_rate_parts[0:2])
                except:
                    pass
            
            # Extract Tx-Power
            if 'Tx-Power=' in line:
                try:
                    tx_power = line.split('Tx-Power=')[1].split(' ')[0]
                    wifi_info['tx_power'] = tx_power
                except:
                    pass
        
        # Try to get additional info from iw if available
        try:
            iw_result = subprocess.check_output(['iw', 'dev', 'wlan0', 'link'], stderr=subprocess.DEVNULL).decode()
            
            for line in iw_result.split('\n'):
                # Get SSID if not already found
                if 'SSID:' in line and not wifi_info['ssid']:
                    wifi_info['ssid'] = line.split('SSID:')[1].strip()
                
                # Get frequency if not already found
                if 'freq:' in line and not wifi_info['frequency']:
                    freq_mhz = line.split('freq:')[1].strip().split()[0]
                    try:
                        freq_ghz = float(freq_mhz) / 1000
                        wifi_info['frequency'] = f"{freq_ghz:.1f} GHz"
                        
                        # Determine band
                        if 2400 <= float(freq_mhz) < 2500:
                            wifi_info['band'] = '2.4 GHz'
                        elif 5000 <= float(freq_mhz) < 6000:
                            wifi_info['band'] = '5 GHz'
                        elif float(freq_mhz) >= 6000:
                            wifi_info['band'] = '6 GHz (WiFi 6E)'
                    except:
                        pass
                
                # Get signal strength in dBm
                if 'signal:' in line and not wifi_info['signal_strength']:
                    signal = line.split('signal:')[1].strip().split()[0]
                    wifi_info['signal_strength'] = f"{signal} dBm"
                    
                    # Calculate quality
                    try:
                        dbm = int(signal)
                        quality = min(100, max(0, 2 * (dbm + 100)))
                        wifi_info['signal_quality'] = f"{quality}%"
                    except:
                        pass
                
                # Get tx bitrate
                if 'tx bitrate:' in line and not wifi_info['bit_rate']:
                    bit_rate = line.split('tx bitrate:')[1].strip()
                    wifi_info['bit_rate'] = bit_rate
        except:
            pass  # iw command not available or failed
        
        return wifi_info
        
    except Exception as e:
        logger.error(f"Error getting WiFi details: {e}", exc_info=True)
        return wifi_info


def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=3)
        return response.json()['ip']
    except:
        return None


def get_audio_devices():
    """Get connected audio devices"""
    try:
        result = subprocess.check_output(['aplay', '-l'], stderr=subprocess.DEVNULL).decode()
        devices = []
        for line in result.split('\n'):
            if 'card' in line.lower():
                devices.append(line.strip())
        return devices
    except:
        return []


def get_weather():
    """Get local weather using wttr.in API with retry logic"""
    max_retries = 2
    timeout_seconds = 3
    
    for attempt in range(max_retries):
        try:
            # Try with increasing timeout on retry
            timeout = timeout_seconds if attempt == 0 else timeout_seconds + 2
            response = requests.get(
                'https://wttr.in/?format=j1', 
                timeout=timeout,
                headers={'User-Agent': 'curl/7.68.0'}  # Some servers prefer curl user agent
            )
            
            if response.status_code != 200:
                if attempt < max_retries - 1:
                    continue
                return None
                
            data = response.json()
            current = data['current_condition'][0]
            
            # Get location info
            location = data.get('nearest_area', [{}])[0]
            location_name = location.get('areaName', [{}])[0].get('value', 'Unknown')
            
            # Get astronomy data for sunrise/sunset
            astronomy = data.get('weather', [{}])[0].get('astronomy', [{}])[0]
            
            return {
                'temperature': int(current['temp_C']),
                'feels_like': int(current['FeelsLikeC']),
                'condition': current['weatherDesc'][0]['value'],
                'description': current['weatherDesc'][0]['value'],
                'humidity': int(current['humidity']),
                'wind_speed': float(current['windspeedKmph']),
                'pressure': int(current.get('pressure', 0)),
                'visibility': int(current.get('visibility', 0)) * 1000,  # Convert km to meters
                'cloudiness': int(current.get('cloudcover', 0)),
                'location': location_name,
                'sunrise': astronomy.get('sunrise', 'N/A').replace('AM', '').strip(),
                'sunset': astronomy.get('sunset', 'N/A').replace('PM', '').strip()
            }
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                continue  # Retry
            logger.warning(f"Weather API timeout after {max_retries} attempts")
            return None
        except Exception as e:
            if attempt < max_retries - 1:
                continue  # Retry on any error
            logger.error(f"Weather API error: {e}", exc_info=True)
            return None
    
    return None


def get_all_stats():
    """Get all system statistics in one call - optimized for dashboard UI"""
    # Only collect stats that the UI actually displays
    # This removes blocking operations and reduces response time from ~9s to <50ms
    
    # CPU stats - non-blocking version
    cpu_percent = psutil.cpu_percent(interval=0)
    cpu_temp = get_cpu_temp()
    
    # Memory stats
    memory = psutil.virtual_memory()
    
    # Disk stats
    disk = psutil.disk_usage('/')
    
    # System info
    uptime = get_uptime()
    
    # Simplified stats - only what the UI needs
    stats = {
        'cpu': {
            'percent': round(cpu_percent, 1),
            'temperature': round(cpu_temp, 1) if cpu_temp else None,
        },
        'memory': {
            'total': round(memory.total / (1024**3), 2),
            'used': round(memory.used / (1024**3), 2),
            'percent': round(memory.percent, 1),
        },
        'disk': {
            'total': round(disk.total / (1024**3), 2),
            'used': round(disk.used / (1024**3), 2),
            'percent': round(disk.percent, 1),
        },
        'system': {
            'uptime': uptime,
        }
    }
    
    return stats


def get_all_stats_detailed():
    """Get all system statistics (verbose version for future use)"""
    # CPU stats - non-blocking version
    cpu_percent = psutil.cpu_percent(interval=0)
    cpu_temp = get_cpu_temp()
    cpu_freq = psutil.cpu_freq()
    cpu_per_core = get_cpu_per_core()
    
    # Memory stats
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Disk stats
    disk = psutil.disk_usage('/')
    partitions = get_partitions()
    
    # Network stats
    network = psutil.net_io_counters()
    network_interfaces = get_network_interfaces()
    active_connections = len(psutil.net_connections())
    
    # System info
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = get_uptime()
    load_avg = os.getloadavg()
    
    # Processes
    process_count = len(psutil.pids())
    top_processes = get_top_processes()
    logged_users = len(psutil.users())
    
    stats = {
        'system_info': {
            'hostname': socket.gethostname(),
            'pi_model': get_pi_model(),
            'os': get_os_info(),
            'architecture': platform.machine(),
            'cpu_cores': psutil.cpu_count(logical=False),
            'cpu_threads': psutil.cpu_count(logical=True),
            'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S')
        },
        'cpu': {
            'percent': round(cpu_percent, 1),
            'temperature': round(cpu_temp, 1) if cpu_temp else None,
            'frequency': round(cpu_freq.current, 0) if cpu_freq else None,
            'frequency_max': round(cpu_freq.max, 0) if cpu_freq else None,
            'per_core': [round(x, 1) for x in cpu_per_core],
            'throttle': get_throttle_status(),
            'load_average': {
                '1min': round(load_avg[0], 2),
                '5min': round(load_avg[1], 2),
                '15min': round(load_avg[2], 2)
            }
        },
        'memory': {
            'total': round(memory.total / (1024**3), 2),
            'used': round(memory.used / (1024**3), 2),
            'percent': round(memory.percent, 1),
            'available': round(memory.available / (1024**3), 2),
            'buffers': round(memory.buffers / (1024**3), 2),
            'cached': round(memory.cached / (1024**3), 2),
            'swap_total': round(swap.total / (1024**3), 2),
            'swap_used': round(swap.used / (1024**3), 2),
            'swap_percent': round(swap.percent, 1),
            'top_processes': top_processes
        },
        'disk': {
            'total': round(disk.total / (1024**3), 2),
            'used': round(disk.used / (1024**3), 2),
            'free': round(disk.free / (1024**3), 2),
            'percent': round(disk.percent, 1),
            'partitions': partitions
        },
        'network': {
            'bytes_sent': round(network.bytes_sent / (1024**2), 2),
            'bytes_recv': round(network.bytes_recv / (1024**2), 2),
            'interfaces': network_interfaces,
            'active_connections': active_connections,
            'wifi_signal': get_wifi_signal(),
            'wifi_details': get_wifi_details(),
            'public_ip': get_public_ip()
        },
        'system': {
            'uptime': uptime,
            'process_count': process_count,
            'logged_users': logged_users,
            'audio_devices': get_audio_devices()
        },
        'weather': get_weather()
    }
    
    return stats

