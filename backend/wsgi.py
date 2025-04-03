from flask import Flask
from flask_migrate import Migrate
from extensions import db, jwt, cors
from api.v1.auth import auth_bp
from api.v1.therapist import therapist_bp
from api.v1.donation import donation_bp
from models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(therapist_bp, url_prefix='/api/v1/therapist')
    app.register_blueprint(donation_bp, url_prefix='/api/v1/donation')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
