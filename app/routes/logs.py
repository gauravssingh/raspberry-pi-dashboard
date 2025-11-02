"""Logs and alerts API routes"""
from flask import Blueprint, jsonify, request
import subprocess
from datetime import datetime, timedelta

logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'logs'})


@logs_bp.route('/services')
def list_services():
    """List available services for log viewing"""
    services = [
        {'id': 'dashboard', 'name': 'Dashboard', 'icon': '📊'},
        {'id': 'raspotify', 'name': 'Raspotify', 'icon': '🎵'},
        {'id': 'shairport-sync', 'name': 'Shairport Sync', 'icon': '📡'},
        {'id': 'nginx', 'name': 'Nginx', 'icon': '🌐'},
        {'id': 'ssh', 'name': 'SSH', 'icon': '🔐'},
        {'id': 'system', 'name': 'System', 'icon': '⚙️'}
    ]
    return jsonify({'services': services})


@logs_bp.route('/view/<service>')
def view_logs(service):
    """View logs for a specific service"""
    lines = request.args.get('lines', 100, type=int)
    lines = min(lines, 1000)  # Maximum 1000 lines
    priority = request.args.get('priority', None)  # emerg, alert, crit, err, warning, notice, info, debug
    since = request.args.get('since', None)  # e.g., "1 hour ago", "30 minutes ago"
    
    # Whitelist of services
    allowed_services = ['dashboard', 'raspotify', 'shairport-sync', 'nginx', 'ssh', 'system', 'kernel']
    
    if service not in allowed_services:
        return jsonify({
            'success': False,
            'error': 'Service not allowed',
            'allowed_services': allowed_services
        }), 400
    
    try:
        # Build journalctl command
        cmd = ['/usr/bin/journalctl', '--no-pager', '-n', str(lines)]
        
        if service != 'system':
            if service == 'kernel':
                cmd.extend(['-k'])  # Kernel logs
            else:
                cmd.extend(['-u', service])
        
        if priority:
            cmd.extend(['-p', priority])
        
        if since:
            cmd.extend(['--since', since])
        
        # Add output format
        cmd.extend(['-o', 'short-iso'])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse logs into structured format
            log_lines = result.stdout.strip().split('\n')
            parsed_logs = []
            
            for line in log_lines:
                if line.strip():
                    parsed_logs.append({
                        'raw': line,
                        'timestamp': line[:25] if len(line) > 25 else '',
                        'message': line[26:] if len(line) > 26 else line
                    })
            
            return jsonify({
                'success': True,
                'service': service,
                'logs': parsed_logs,
                'count': len(parsed_logs),
                'lines_requested': lines
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


@logs_bp.route('/search')
def search_logs():
    """Search logs across all services"""
    query = request.args.get('query', '').strip()
    lines = request.args.get('lines', 100, type=int)
    lines = min(lines, 500)
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter required'
        }), 400
    
    try:
        result = subprocess.run(
            ['/usr/bin/journalctl', '--no-pager', '-n', str(lines), '--grep', query, '-o', 'short-iso'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            log_lines = result.stdout.strip().split('\n')
            parsed_logs = []
            
            for line in log_lines:
                if line.strip():
                    parsed_logs.append({
                        'raw': line,
                        'timestamp': line[:25] if len(line) > 25 else '',
                        'message': line[26:] if len(line) > 26 else line
                    })
            
            return jsonify({
                'success': True,
                'query': query,
                'logs': parsed_logs,
                'count': len(parsed_logs)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Search failed',
                'stderr': result.stderr
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@logs_bp.route('/errors')
def get_errors():
    """Get recent error logs from all services"""
    hours = request.args.get('hours', 1, type=int)
    hours = min(hours, 24)  # Maximum 24 hours
    
    try:
        result = subprocess.run(
            ['/usr/bin/journalctl', '--no-pager', '--since', f'{hours} hours ago', 
             '-p', 'err', '-o', 'short-iso'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            log_lines = result.stdout.strip().split('\n')
            parsed_logs = []
            
            for line in log_lines:
                if line.strip():
                    parsed_logs.append({
                        'raw': line,
                        'timestamp': line[:25] if len(line) > 25 else '',
                        'message': line[26:] if len(line) > 26 else line
                    })
            
            return jsonify({
                'success': True,
                'logs': parsed_logs,
                'count': len(parsed_logs),
                'timeframe': f'{hours} hours'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve errors',
                'stderr': result.stderr
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@logs_bp.route('/boot')
def get_boot_logs():
    """Get logs from current boot"""
    try:
        result = subprocess.run(
            ['/usr/bin/journalctl', '--no-pager', '-b', '-o', 'short-iso'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            log_lines = result.stdout.strip().split('\n')
            parsed_logs = []
            
            for line in log_lines:
                if line.strip():
                    parsed_logs.append({
                        'raw': line,
                        'timestamp': line[:25] if len(line) > 25 else '',
                        'message': line[26:] if len(line) > 26 else line
                    })
            
            return jsonify({
                'success': True,
                'logs': parsed_logs,
                'count': len(parsed_logs)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve boot logs',
                'stderr': result.stderr
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@logs_bp.route('/follow/<service>')
def follow_logs(service):
    """Get recent logs for live following (last 20 lines)"""
    allowed_services = ['dashboard', 'raspotify', 'shairport-sync', 'nginx', 'ssh', 'system']
    
    if service not in allowed_services:
        return jsonify({
            'success': False,
            'error': 'Service not allowed'
        }), 400
    
    try:
        cmd = ['/usr/bin/journalctl', '--no-pager', '-n', '20', '-o', 'short-iso']
        
        if service != 'system':
            cmd.extend(['-u', service])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            log_lines = result.stdout.strip().split('\n')
            parsed_logs = []
            
            for line in log_lines:
                if line.strip():
                    parsed_logs.append({
                        'raw': line,
                        'timestamp': line[:25] if len(line) > 25 else '',
                        'message': line[26:] if len(line) > 26 else line
                    })
            
            return jsonify({
                'success': True,
                'service': service,
                'logs': parsed_logs,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to retrieve logs'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

