"""Flask application configuration"""
import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JSON_SORT_KEYS = False
    
    # Optimize for Raspberry Pi 3B (1GB RAM)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    
    # Cache settings
    SEND_FILE_MAX_AGE_DEFAULT = 300  # 5 minutes for static files

    # System configuration - will be populated at runtime
    LOCAL_IP = None
    HOSTNAME = None


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration - optimized for Pi 3B"""
    DEBUG = False
    TESTING = False
    
    # Nginx proxy settings
    PREFERRED_URL_SCHEME = 'http'
    
    # Security headers (nginx will handle most, but good to have)
    SESSION_COOKIE_SECURE = False  # Set True if using HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}

