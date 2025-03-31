# config/config.py
import os
from datetime import timedelta
from dotenv import load_dotenv
from .mpesa import MPESAConfig

# Load environment variables from .env file
load_dotenv()

class BaseConfig:
    """Base configuration class for Mind Wellness API"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-here')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ERROR_MESSAGE_KEY = 'message'
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # API Configuration
    API_TITLE = 'Mind Wellness API'
    API_VERSION = 'v1'
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    CORS_SUPPORTS_CREDENTIALS = True
    
    # MPESA Configuration
    MPESA = MPESAConfig

class DevelopmentConfig(BaseConfig):
    """Development configuration for Mind Wellness API"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    
    # Development-specific settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  # Longer expiry for development
    
    @property
    def MPESA_ENVIRONMENT(self):
        return 'sandbox'

class TestingConfig(BaseConfig):
    """Testing configuration for Mind Wellness API"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Test-specific settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    
    @property
    def MPESA_ENVIRONMENT(self):
        return 'sandbox'

class ProductionConfig(BaseConfig):
    """Production configuration for Mind Wellness API"""
    DEBUG = False
    TESTING = False
    
    # Production-specific security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Additional security headers (optional)
    # SECURITY_HEADERS = {
    #     'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    #     'X-Content-Type-Options': 'nosniff',
    #     'X-Frame-Options': 'SAMEORIGIN',
    #     'X-XSS-Protection': '1; mode=block',
    # }
    
    @property
    def MPESA_ENVIRONMENT(self):
        return 'production'
    
    def __init__(self):
        super().__init__()
        self.validate_production_settings()
    
    def validate_production_settings(self):
        """Validate required production settings for Mind Wellness API"""
        required_settings = [
            'SECRET_KEY',
            'JWT_SECRET_KEY',
            'DATABASE_URL',
            'MPESA_CONSUMER_KEY',
            'MPESA_CONSUMER_SECRET',
            'MPESA_SHORTCODE',
            'MPESA_PASSKEY',
            'MPESA_CALLBACK_URL'
        ]
        
        missing_settings = [
            setting for setting in required_settings 
            if not os.getenv(setting)
        ]
        
        if missing_settings:
            raise ValueError(
                f"Missing required production settings: {', '.join(missing_settings)}"
            )

def get_config(config_name=None):
    """Helper function to get configuration class for Mind Wellness API"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
