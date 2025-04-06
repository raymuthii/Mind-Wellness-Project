"""API v1 package"""
from flask import Blueprint

# Create blueprints
auth_bp = Blueprint('auth', __name__)
therapist_bp = Blueprint('therapist', __name__)
appointment_bp = Blueprint('appointment', __name__)
donation_bp = Blueprint('donation', __name__)

# Import routes after blueprint creation to avoid circular imports
from backend.api.v1.auth import init_auth_routes
from backend.api.v1.therapist import init_therapist_routes
from backend.api.v1.appointment import init_appointment_routes
from backend.api.v1.donation import init_donation_routes

# Initialize routes
init_auth_routes(auth_bp)
init_therapist_routes(therapist_bp)
init_appointment_routes(appointment_bp)
init_donation_routes(donation_bp)

# Make blueprints available at package level
__all__ = ['auth_bp', 'therapist_bp', 'appointment_bp', 'donation_bp'] 