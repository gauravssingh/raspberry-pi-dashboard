"""Services API routes - control and monitor various services"""
from flask import Blueprint, jsonify
from app.modules import raspotify, shairport_sync

services_bp = Blueprint('services', __name__)


@services_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'services'})


@services_bp.route('/raspotify/status')
def raspotify_status():
    """Get Raspotify service status"""
    status = raspotify.get_service_status()
    device_name = raspotify.get_device_name()
    
    return jsonify({
        'service': 'raspotify',
        'device_name': device_name,
        **status
    })


@services_bp.route('/raspotify/current')
def raspotify_current():
    """Get currently playing track on Raspotify"""
    current = raspotify.get_current_track()
    
    return jsonify({
        'service': 'raspotify',
        **current
    })


@services_bp.route('/shairport-sync/status')
def shairport_status():
    """Get Shairport Sync service status"""
    status = shairport_sync.get_service_status()
    device_name = shairport_sync.get_device_name()
    
    return jsonify({
        'service': 'shairport-sync',
        'device_name': device_name,
        **status
    })


@services_bp.route('/shairport-sync/current')
def shairport_current():
    """Get current playback on Shairport Sync"""
    current = shairport_sync.get_current_playback()
    
    return jsonify({
        'service': 'shairport-sync',
        **current
    })


@services_bp.route('/list')
def list_services():
    """List all available services"""
    services = [
        {
            'name': 'Raspotify',
            'id': 'raspotify',
            'description': 'Spotify Connect for Raspberry Pi',
            'endpoints': {
                'status': '/api/services/raspotify/status',
                'current': '/api/services/raspotify/current'
            }
        },
        {
            'name': 'Shairport Sync',
            'id': 'shairport-sync',
            'description': 'AirPlay Audio Receiver',
            'endpoints': {
                'status': '/api/services/shairport-sync/status',
                'current': '/api/services/shairport-sync/current'
            }
        }
        # Add more services here as you integrate them
    ]
    
    return jsonify({'services': services})

