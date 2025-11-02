"""System API routes - system information and monitoring"""
from flask import Blueprint, jsonify, current_app
from app.modules import system_monitor

system_bp = Blueprint('system', __name__)


@system_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'system'})


@system_bp.route('/stats')
def stats():
    """Get quick system statistics - optimized for dashboard"""
    try:
        stats = system_monitor.get_all_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/info')
def system_info():
    """Get detailed system information"""
    try:
        stats = system_monitor.get_all_stats_detailed()
        
        # Add Flask config system info
        stats['system_info']['local_ip'] = current_app.config.get('LOCAL_IP', 'unknown')
        stats['system_info']['hostname'] = current_app.config.get('HOSTNAME', 'unknown')
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/network-stats')
def network_stats():
    """Get network statistics"""
    try:
        import psutil
        network = psutil.net_io_counters()
        
        return jsonify({
            'bytes_sent': round(network.bytes_sent / (1024**2), 2),
            'bytes_recv': round(network.bytes_recv / (1024**2), 2),
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv,
            'errors_in': network.errin,
            'errors_out': network.errout,
            'drops_in': network.dropin,
            'drops_out': network.dropout
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/network/interfaces')
def network_interfaces():
    """Get network interface information"""
    try:
        interfaces = system_monitor.get_network_interfaces()
        
        # Add local IP from config
        local_ip = current_app.config.get('LOCAL_IP')
        if local_ip:
            interfaces['_primary'] = {'ip': local_ip}
        
        return jsonify({
            'success': True,
            'interfaces': interfaces,
            'local_ip': local_ip
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/network/public-ip')
def public_ip():
    """Get public IP address"""
    try:
        ip = system_monitor.get_public_ip()
        return jsonify({
            'success': True,
            'public_ip': ip
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/wifi-details')
def wifi_details():
    """Get detailed WiFi information"""
    try:
        wifi_info = system_monitor.get_wifi_details()
        return jsonify({
            'success': True,
            'wifi': wifi_info
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/weather')
def weather():
    """Get weather information"""
    try:
        weather_data = system_monitor.get_weather()
        if weather_data:
            return jsonify({
                'success': True,
                'weather': weather_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Weather data unavailable'
            }), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/config')
def system_config():
    """Get system configuration including IP and hostname"""
    try:
        return jsonify({
            'success': True,
            'config': {
                'local_ip': current_app.config.get('LOCAL_IP'),
                'hostname': current_app.config.get('HOSTNAME'),
                'system_config': current_app.config.get('SYSTEM_CONFIG', {})
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@system_bp.route('/world-clocks')
def world_clocks():
    """Get current time in various time zones"""
    try:
        from datetime import datetime
        import pytz
        
        # Define time zones to display
        timezones = [
            {'name': 'Local', 'timezone': 'Asia/Kolkata', 'city': 'India'},
            {'name': 'New York', 'timezone': 'America/New_York', 'city': 'USA'},
            {'name': 'London', 'timezone': 'Europe/London', 'city': 'UK'},
            {'name': 'Tokyo', 'timezone': 'Asia/Tokyo', 'city': 'Japan'},
            {'name': 'Sydney', 'timezone': 'Australia/Sydney', 'city': 'Australia'},
            {'name': 'Dubai', 'timezone': 'Asia/Dubai', 'city': 'UAE'},
            {'name': 'Singapore', 'timezone': 'Asia/Singapore', 'city': 'Singapore'},
            {'name': 'Los Angeles', 'timezone': 'America/Los_Angeles', 'city': 'USA'}
        ]
        
        clocks = []
        for tz_info in timezones:
            try:
                tz = pytz.timezone(tz_info['timezone'])
                current_time = datetime.now(tz)
                
                clocks.append({
                    'name': tz_info['name'],
                    'city': tz_info['city'],
                    'timezone': tz_info['timezone'],
                    'time': current_time.strftime('%H:%M:%S'),
                    'date': current_time.strftime('%Y-%m-%d'),
                    'day': current_time.strftime('%A'),
                    'offset': current_time.strftime('%z'),
                    'offset_hours': current_time.strftime('%z')[:3] + ':' + current_time.strftime('%z')[3:]
                })
            except Exception as e:
                current_app.logger.error(f"Error getting time for {tz_info['name']}: {e}")
                continue
        
        return jsonify({
            'success': True,
            'clocks': clocks,
            'count': len(clocks)
        })
    except Exception as e:
        current_app.logger.error(f"Error getting world clocks: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
