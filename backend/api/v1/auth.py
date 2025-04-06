"""Authentication endpoints"""
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import logging

from backend.models import User, db

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock user for testing
MOCK_USER = {
    'email': 'test@example.com',
    'password': 'test123'
}

def init_auth_routes(bp):
    @bp.route('/register', methods=['POST'])
    def register():
        """Register endpoint"""
        try:
            data = request.get_json()
            logger.info(f"Received registration request for email: {data.get('email', 'no email provided')}")
            
            if not data or not all(k in data for k in ('name', 'email', 'password')):
                logger.error("Missing required fields in registration request")
                return jsonify({'error': 'Missing required fields'}), 400
                
            # Check if user already exists
            if User.query.filter_by(email=data['email']).first():
                logger.warning(f"Registration attempt with existing email: {data['email']}")
                return jsonify({'error': 'Email already registered'}), 400
                
            # Create new user
            new_user = User(
                name=data['name'],
                email=data['email'],
                password_hash=generate_password_hash(data['password']),
                role='patient'  # Default role is patient
            )
            
            try:
                db.session.add(new_user)
                db.session.commit()
                logger.info(f"Successfully created new user with email: {data['email']}")
                
                # Create access token
                access_token = create_access_token(
                    identity=new_user.email,
                    expires_delta=timedelta(days=1)
                )
                
                return jsonify({
                    'user': {
                        'email': new_user.email,
                        'name': new_user.name,
                        'role': new_user.role
                    },
                    'access_token': access_token,
                    'token_type': 'bearer'
                }), 201
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"Database error during user creation: {str(e)}")
                return jsonify({'error': 'Failed to create user: Database error'}), 500
                
        except Exception as e:
            logger.error(f"Unexpected error in registration: {str(e)}")
            return jsonify({'error': f'Registration failed: {str(e)}'}), 500

    @bp.route('/login', methods=['POST'])
    def login():
        """Login endpoint"""
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
            
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
            
        # Create access token
        access_token = create_access_token(
            identity=user.email,
            expires_delta=timedelta(days=1)
        )
        
        return jsonify({
            'user': {
                'email': user.email,
                'name': user.name,
                'role': user.role
            },
            'access_token': access_token,
            'token_type': 'bearer'
        }), 200

    @bp.route('/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        """Get current user endpoint"""
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'email': user.email,
            'name': user.name,
            'role': user.role,
            'is_authenticated': True
        }), 200

# Initialize routes with the auth blueprint
auth_bp = Blueprint('auth', __name__)
init_auth_routes(auth_bp) 