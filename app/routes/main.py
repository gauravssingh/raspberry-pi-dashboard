"""Main page routes - renders HTML templates"""
from flask import Blueprint, render_template, send_from_directory
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Dashboard homepage"""
    return render_template('index.html')


@main_bp.route('/services')
def services():
    """Services status page"""
    return render_template('services.html')


@main_bp.route('/configuration')
def configuration():
    """Configuration page - network and device settings"""
    return render_template('configuration.html')


@main_bp.route('/tools')
def tools():
    """Tools page - system actions, diagnostics, terminal"""
    return render_template('tools.html')


@main_bp.route('/settings')
def settings():
    """Settings page - preferences and customization"""
    return render_template('settings.html')


@main_bp.route('/weather')
def weather():
    """Weather and world clocks page"""
    return render_template('weather.html')


@main_bp.route('/docs')
def docs():
    """Documentation page"""
    return render_template('docs.html')


@main_bp.route('/logs')
def logs():
    """Logs and alerts page"""
    return render_template('logs.html')


@main_bp.route('/gpio')
def gpio():
    """GPIO control page"""
    return render_template('gpio.html')


@main_bp.route('/gpio/wiring')
def gpio_wiring():
    """GPIO wiring guide page"""
    return render_template('gpio_wiring.html')


@main_bp.route('/docs/<path:filename>')
def serve_docs(filename):
    """Serve documentation files"""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    return send_from_directory(docs_dir, filename)
