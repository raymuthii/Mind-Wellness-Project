"""Backend package"""
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from extensions import db, jwt, cors
from api.v1.auth import auth_bp
from api.v1.therapist import therapist_bp
from api.v1.appointment import appointment_bp

def create_app(config=None):
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
    cors.init_app(app)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to Mind Wellness API',
            'version': '1.0',
            'endpoints': {
                'auth': '/api/v1/auth',
                'therapist': '/api/v1/therapist',
                'appointment': '/api/v1/appointment'
            }
        })
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(therapist_bp, url_prefix='/api/v1')
    app.register_blueprint(appointment_bp, url_prefix='/api/v1')
    
    return app 