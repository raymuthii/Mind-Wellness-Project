from flask import Flask
from dotenv import load_dotenv
import os

# Import the extensions from a single source
from backend.extensions import db, migrate, ma, jwt, cors, mail, init_app

def create_app(config_name=None):
    app = Flask(__name__)
    load_dotenv()
    
    # Configuration
    app.config.from_object(config_name)
    
    # Use the init_app function from extensions to initialize all extensions
    init_app(app)
    
    with app.app_context():
        # Import routes (updated for mental health platform)
        from backend.routes import (
            auth_bp, 
            provider_bp,         # Renamed from charity_bp to provider_bp
            donation_bp, 
            success_story_bp,    # Renamed from story_bp to success_story_bp
            user_bp, 
            admin_bp, 
            provider_admin_bp     # Renamed from charity_admin_bp to provider_admin_bp
        )
        
        # Register blueprints with updated URL prefixes
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(provider_bp, url_prefix='/api/providers')
        app.register_blueprint(donation_bp, url_prefix='/api/donations')
        app.register_blueprint(success_story_bp, url_prefix='/api/success-stories')
        app.register_blueprint(user_bp, url_prefix='/api/users')
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
        app.register_blueprint(provider_admin_bp, url_prefix='/api/provider-admin')
        
        # Create database tables
        db.create_all()    
    return app
