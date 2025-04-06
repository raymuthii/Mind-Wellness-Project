"""Backend package"""
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from backend.extensions import db, jwt, cors

def create_app(config=None):
    """Create Flask application."""
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-key-change-in-prod')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours
    
    # Override with provided config
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # CORS Configuration
    cors.init_app(app, resources={
        r"/*": {
            "origins": ["http://localhost:3001"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"],
            "max_age": 600,  # Cache preflight requests for 10 minutes
            "send_wildcard": False,
            "automatic_options": True
        }
    })
    
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from backend.models import User, Donation, Testimonial, SuccessStory, Appointment
        
        # Import blueprints
        from backend.api.v1.auth import auth_bp
        from backend.api.v1.therapist import therapist_bp
        from backend.api.v1.appointment import appointment_bp
        from backend.api.v1.donation import donation_bp
        
        # Register blueprints
        app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
        app.register_blueprint(therapist_bp, url_prefix='/api/v1/therapist')
        app.register_blueprint(appointment_bp, url_prefix='/api/v1')
        app.register_blueprint(donation_bp, url_prefix='/api/v1/donation')
        
        # Root route
        @app.route('/')
        def index():
            return jsonify({
                'message': 'Welcome to Mind Wellness API',
                'version': '1.0',
                'endpoints': {
                    'auth': '/api/v1/auth',
                    'therapist': '/api/v1/therapist',
                    'appointments': '/api/v1/appointments',
                    'donation': '/api/v1/donation'
                }
            })
        
        return app 