"""Flask extensions"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

# Make extensions available at package level
__all__ = ['db', 'jwt', 'cors'] 