"""Authentication routes"""
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv

from . import auth_bp
from models import User

# Load environment variables
load_dotenv()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
        
    # For testing purposes, accept any email/password
    access_token = create_access_token(
        identity=data['email'],
        expires_delta=timedelta(days=1)
    )
    
    return jsonify({
        'access_token': access_token,
        'token_type': 'bearer'
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user endpoint"""
    current_user_email = get_jwt_identity()
    return jsonify({
        'email': current_user_email,
        'is_authenticated': True
    }), 200 