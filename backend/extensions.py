from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()
mail = Mail()

def init_app(app):
    # Load environment variables and configuration for Mind Wellness platform
    if os.getenv('FLASK_ENV') == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Initialize all extensions with the Flask app
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            'status': 401,
            'message': 'The token has expired',
            'error': 'token_expired'
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            'status': 401,
            'message': 'Invalid token',
            'error': 'invalid_token'
        }, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            'status': 401,
            'message': 'Token is missing',
            'error': 'authorization_required'
        }, 401

    # Add custom claims to JWT tokens for Mind Wellness
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        return {
            'user_id': identity,
            # Add more claims as needed for Mind Wellness
        }

    # CORS Configuration for API endpoints
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"],  # Update this URL to your actual frontend URL in production
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
