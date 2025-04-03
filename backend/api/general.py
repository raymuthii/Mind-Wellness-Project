"""General routes"""
from flask import Blueprint, jsonify

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'name': 'Mind Wellness API',
        'version': '1.0',
        'description': 'API for Mind Wellness donation platform',
        'endpoints': {
            'auth': {
                'login': '/api/v1/auth/login',
                'me': '/api/v1/auth/me'
            },
            'donations': {
                'create': '/api/v1/donations/',
                'list': '/api/v1/donations/',
                'webhook': '/api/v1/donations/webhook'
            }
        }
    }) 