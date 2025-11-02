"""Logging configuration for Flask application"""
import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(app):
    """Configure application logging"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Log level from environment or default to INFO
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    
    # Configure root logger
    app.logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Remove default handlers
    app.logger.handlers.clear()
    
    # File handler for application logs
    log_file = log_dir / 'app.log'
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    
    # Error file handler for errors and above
    error_log_file = log_dir / 'error.log'
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    
    # Console handler for development
    if app.config.get('DEBUG'):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        app.logger.addHandler(console_handler)
    
    # Add handlers
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_handler)
    
    # Set log level for Werkzeug (Flask's underlying WSGI library)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.WARNING)
    
    # Set log level for gunicorn
    gunicorn_logger = logging.getLogger('gunicorn')
    gunicorn_logger.setLevel(logging.INFO)
    
    app.logger.info(f'Logging configured. Log files: {log_dir}/app.log, {log_dir}/error.log')
    
    return app.logger


def get_logger(name):
    """Get a logger instance for a module"""
    return logging.getLogger(name)

