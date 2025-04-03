"""API v1 routes"""
from flask import Blueprint

# Create blueprints for Mind Wellness platform
auth_bp = Blueprint('auth', __name__)
donation_bp = Blueprint('donation', __name__)

# Import routes after blueprint creation to avoid circular imports
from . import auth, donation

# Make blueprints available at package level
__all__ = ['auth_bp', 'donation_bp'] 