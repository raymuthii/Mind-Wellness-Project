from flask import Flask
from backend.extensions import db, migrate, ma, jwt, cors, mail, init_app

def create_app():
    """Flask application factory"""
    app = Flask(__name__)

    # Initialize extensions
    init_app(app)

    # Register blueprints here (if any)
    # from backend.routes import main_bp
    # app.register_blueprint(main_bp)

    return app
