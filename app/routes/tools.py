"""Tools API routes - system actions, diagnostics, terminal"""
from flask import Blueprint, jsonify, request
import subprocess
import os
from functools import lru_cache
import time

tools_bp = Blueprint('tools', __name__)

# Cache for preventing rapid repeated actions
_action_cache = {}

def rate_limit_action(action_name, cooldown_seconds=5):
    """Rate limit system actions to prevent abuse"""
    now = time.time()
    if action_name in _action_cache:
        last_time = _action_cache[action_name]
        if now - last_time < cooldown_seconds:
            return False
    _action_cache[action_name] = now
    return True


@tools_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'tools'})


@tools_bp.route('/system/info')
def system_info():
    """Get system action information and capabilities"""
    return jsonify({
        'available_actions': [
            {'id': 'reboot', 'name': 'Reboot System', 'icon': '🔄', 'dangerous': True},
            {'id': 'shutdown', 'name': 'Shutdown', 'icon': '⚡', 'dangerous': True},
            {'id': 'restart_dashboard', 'name': 'Restart Dashboard', 'icon': '🔃', 'dangerous': False},
            {'id': 'restart_raspotify', 'name': 'Restart Raspotify', 'icon': '🎵', 'dangerous': False},
            {'id': 'restart_shairport', 'name': 'Restart Shairport', 'icon': '📡', 'dangerous': False}
        ],
        'permissions': {
            'can_reboot': os.access('/sbin/reboot', os.X_OK),
            'can_shutdown': os.access('/sbin/shutdown', os.X_OK),
            'can_manage_services': os.access('/bin/systemctl', os.X_OK)
        }
    })


@tools_bp.route('/diagnostics')
def diagnostics():
    """Run system diagnostics"""
    diagnostics_data = {
        'system': {},
        'services': {},
        'connectivity': {},
        'storage': {}
    }
    
    # System checks
    try:
        # Check if system is responsive
        result = subprocess.run(['/usr/bin/uptime'], capture_output=True, text=True, timeout=2)
        diagnostics_data['system']['responsive'] = result.returncode == 0
        diagnostics_data['system']['load_average'] = result.stdout.strip().split('load average:')[-1].strip() if result.returncode == 0 else 'N/A'
    except Exception as e:
        diagnostics_data['system']['responsive'] = False
        diagnostics_data['system']['error'] = str(e)
    
    # Check critical services
    services_to_check = ['dashboard', 'raspotify', 'shairport-sync', 'nginx', 'ssh']
    for service in services_to_check:
        try:
            result = subprocess.run(['/usr/bin/systemctl', 'is-active', service], 
                                  capture_output=True, text=True, timeout=2)
            diagnostics_data['services'][service] = {
                'status': result.stdout.strip(),
                'healthy': result.returncode == 0
            }
        except Exception as e:
            diagnostics_data['services'][service] = {
                'status': 'error',
                'healthy': False,
                'error': str(e)
            }
    
    # Connectivity checks
    try:
        # Check internet connectivity
        result = subprocess.run(['/usr/bin/ping', '-c', '1', '-W', '2', '8.8.8.8'], 
                              capture_output=True, timeout=3)
        diagnostics_data['connectivity']['internet'] = result.returncode == 0
    except:
        diagnostics_data['connectivity']['internet'] = False
    
    try:
        # Check DNS
        result = subprocess.run(['/usr/bin/ping', '-c', '1', '-W', '2', 'google.com'], 
                              capture_output=True, timeout=3)
        diagnostics_data['connectivity']['dns'] = result.returncode == 0
    except:
        diagnostics_data['connectivity']['dns'] = False
    
    # Storage checks
    try:
        result = subprocess.run(['/usr/bin/df', '-h', '/'], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                diagnostics_data['storage']['root'] = {
                    'total': parts[1],
                    'used': parts[2],
                    'available': parts[3],
                    'use_percent': parts[4]
                }
    except Exception as e:
        diagnostics_data['storage']['error'] = str(e)
    
    return jsonify(diagnostics_data)


@tools_bp.route('/execute', methods=['POST'])
def execute_command():
    """Execute a terminal command (restricted for security)"""
    data = request.get_json()
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'success': False, 'error': 'No command provided'}), 400
    
    # Whitelist of safe commands (with full paths)
    safe_commands = [
        '/usr/bin/uptime', '/usr/bin/date', '/usr/bin/whoami', '/usr/bin/hostname', '/usr/bin/uname',
        '/usr/bin/df', '/usr/bin/free', '/usr/bin/ps', '/usr/bin/top', '/usr/bin/htop',
        '/usr/sbin/ip addr', '/usr/sbin/ip link', '/usr/sbin/iwconfig',
        '/usr/bin/systemctl status', '/usr/bin/journalctl',
        '/usr/bin/vcgencmd measure_temp', '/usr/bin/vcgencmd get_throttled',
        '/usr/bin/ls', '/usr/bin/pwd', '/usr/bin/cat /proc/cpuinfo', '/usr/bin/cat /proc/meminfo',
        # Also allow without full paths for user convenience
        'uptime', 'date', 'whoami', 'hostname', 'uname',
        'df', 'free', 'ps', 'top', 'htop',
        'ip addr', 'ip link', 'iwconfig',
        'systemctl status', 'journalctl',
        'vcgencmd measure_temp', 'vcgencmd get_throttled',
        'ls', 'pwd', 'cat /proc/cpuinfo', 'cat /proc/meminfo'
    ]
    
    # Check if command starts with any safe command
    is_safe = any(command.startswith(safe_cmd) for safe_cmd in safe_commands)
    
    if not is_safe:
        return jsonify({
            'success': False,
            'error': 'Command not allowed',
            'message': 'For security reasons, only whitelisted commands are allowed',
            'allowed_commands': safe_commands
        }), 403
    
    try:
        # Execute command with timeout and proper PATH
        env = os.environ.copy()
        env['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.expanduser('~'),
            env=env
        )
        
        return jsonify({
            'success': True,
            'command': command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Command timed out',
            'message': 'Command execution exceeded 10 second timeout'
        }), 408
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Execution failed',
            'message': str(e)
        }), 500


@tools_bp.route('/logs/<service>')
def get_service_logs(service):
    """Get logs for a specific service"""
    lines = request.args.get('lines', 50, type=int)
    lines = min(lines, 500)  # Maximum 500 lines
    
    # Whitelist of services
    allowed_services = ['dashboard', 'raspotify', 'shairport-sync', 'nginx', 'ssh', 'system']
    
    if service not in allowed_services:
        return jsonify({
            'success': False,
            'error': 'Service not allowed',
            'allowed_services': allowed_services
        }), 400
    
    try:
        if service == 'system':
            # System-wide logs
            result = subprocess.run(
                ['/usr/bin/journalctl', '-n', str(lines), '--no-pager'],
                capture_output=True,
                text=True,
                timeout=5
            )
        else:
            # Service-specific logs
            result = subprocess.run(
                ['/usr/bin/journalctl', '-u', service, '-n', str(lines), '--no-pager'],
                capture_output=True,
                text=True,
                timeout=5
            )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'service': service,
                'logs': result.stdout,
                'lines': lines
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve logs',
                'stderr': result.stderr
            }), 500
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Log retrieval timed out'
        }), 408
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tools_bp.route('/action/<action_name>', methods=['POST'])
def system_action(action_name):
    """Execute a system action (reboot, shutdown, etc.)"""
    
    # Rate limiting
    if not rate_limit_action(action_name):
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded',
            'message': 'Please wait before executing this action again'
        }), 429
    
    # Get confirmation flag
    data = request.get_json() or {}
    confirmed = data.get('confirmed', False)
    
    if not confirmed:
        return jsonify({
            'success': False,
            'error': 'Confirmation required',
            'message': 'This action requires confirmation'
        }), 400
    
    actions = {
        'reboot': {
            'command': ['sudo', 'reboot'],
            'description': 'System will reboot'
        },
        'shutdown': {
            'command': ['sudo', 'shutdown', '-h', 'now'],
            'description': 'System will shutdown'
        },
        'restart_dashboard': {
            'command': ['sudo', 'systemctl', 'restart', 'dashboard'],
            'description': 'Dashboard service will restart'
        },
        'restart_raspotify': {
            'command': ['sudo', 'systemctl', 'restart', 'raspotify'],
            'description': 'Raspotify service will restart'
        },
        'restart_shairport': {
            'command': ['sudo', 'systemctl', 'restart', 'shairport-sync'],
            'description': 'Shairport Sync service will restart'
        }
    }
    
    if action_name not in actions:
        return jsonify({
            'success': False,
            'error': 'Unknown action',
            'available_actions': list(actions.keys())
        }), 400
    
    action = actions[action_name]
    
    try:
        # Execute action
        subprocess.Popen(action['command'])
        
        return jsonify({
            'success': True,
            'action': action_name,
            'message': action['description']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Action failed',
            'message': str(e)
        }), 500

