"""API v1 package"""
from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__)
donation_bp = Blueprint('donation', __name__)

# Import routes after blueprint creation to avoid circular imports
import api.v1.auth
import api.v1.donation

# Make blueprints available at package level
__all__ = ['auth_bp', 'donation_bp'] 