"""Flask application factory"""
from flask import Flask
from flask_cors import CORS


def create_app(config_name='production'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Setup logging
    from app.logging_config import setup_logging
    setup_logging(app)
    
    # Load system information
    from app.system_info import SYSTEM_CONFIG, LOCAL_IP, HOSTNAME
    app.config['LOCAL_IP'] = LOCAL_IP
    app.config['HOSTNAME'] = HOSTNAME
    app.config['SYSTEM_CONFIG'] = SYSTEM_CONFIG
    app.logger.info(f"System configured - IP: {LOCAL_IP}, Hostname: {HOSTNAME}")
    
    # Make system config available in all templates
    @app.context_processor
    def inject_system_config():
        return {
            'LOCAL_IP': LOCAL_IP,
            'HOSTNAME': HOSTNAME,
            'SYSTEM_CONFIG': SYSTEM_CONFIG
        }
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.system import system_bp
    from app.routes.services import services_bp
    from app.routes.tools import tools_bp
    from app.routes.logs import logs_bp
    from app.routes.gpio import gpio_bp
    from app.routes.mqtt import mqtt_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(system_bp, url_prefix='/api/system')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(tools_bp, url_prefix='/api/tools')
    app.register_blueprint(logs_bp, url_prefix='/api/logs')
    app.register_blueprint(gpio_bp, url_prefix='/api/gpio')
    app.register_blueprint(mqtt_bp, url_prefix='/api/mqtt')
    
    app.logger.info('Flask application initialized')
    
    return app

