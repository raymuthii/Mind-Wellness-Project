"""Therapist endpoints"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import logging
from werkzeug.security import generate_password_hash
from datetime import timedelta

from models import User, db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_therapist_routes(bp):
    @bp.route('/therapist/register', methods=['POST'])
    def register_therapist():
        """Register a new therapist"""
        try:
            data = request.get_json()
            logger.info(f"Received therapist registration data: {data}")
            
            required_fields = ['name', 'email', 'password', 'specialization', 'bio', 'years_of_experience', 'hourly_rate']
            
            # Log which fields are missing
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                logger.error(f"Missing required fields: {missing_fields}")
                return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
            
            # Check if user already exists
            if User.query.filter_by(email=data['email']).first():
                logger.warning(f"Registration attempt with existing email: {data['email']}")
                return jsonify({'error': 'Email already registered'}), 400
            
            try:
                years_of_experience = int(data['years_of_experience'])
                hourly_rate = float(data['hourly_rate'])
            except (ValueError, TypeError) as e:
                logger.error(f"Invalid numeric values: {str(e)}")
                return jsonify({'error': 'Invalid years of experience or hourly rate'}), 400
            
            # Create new therapist
            new_therapist = User(
                name=data['name'],
                email=data['email'],
                password_hash=generate_password_hash(data['password']),
                role='therapist',
                specialization=data['specialization'],
                bio=data['bio'],
                years_of_experience=years_of_experience,
                hourly_rate=hourly_rate,
                availability=data.get('availability', {}),
                profile_image=data.get('profile_image'),
                qualifications=data.get('qualifications', []),
                languages=data.get('languages', ['English']),
                is_verified=False
            )
            
            db.session.add(new_therapist)
            db.session.commit()
            logger.info(f"Successfully created new therapist with email: {data['email']}")
            
            # Create access token
            access_token = create_access_token(
                identity=new_therapist.email,
                expires_delta=timedelta(days=1)
            )
            
            return jsonify({
                'message': 'Therapist registered successfully',
                'therapist': new_therapist.to_dict(),
                'access_token': access_token,
                'token_type': 'bearer'
            }), 201
            
        except Exception as e:
            logger.error(f"Error registering therapist: {str(e)}")
            db.session.rollback()
            return jsonify({'error': f'Failed to register therapist: {str(e)}'}), 500

    @bp.route('/therapists', methods=['GET'])
    def get_therapists():
        """Get list of all verified therapists"""
        try:
            # Get query parameters for filtering
            specialization = request.args.get('specialization')
            min_experience = request.args.get('min_experience', type=int)
            max_rate = request.args.get('max_rate', type=float)
            language = request.args.get('language')
            
            # Base query
            query = User.query.filter_by(role='therapist', is_verified=True)
            
            # Apply filters
            if specialization:
                query = query.filter(User.specialization == specialization)
            if min_experience:
                query = query.filter(User.years_of_experience >= min_experience)
            if max_rate:
                query = query.filter(User.hourly_rate <= max_rate)
            if language:
                query = query.filter(User.languages.contains([language]))
            
            therapists = query.all()
            return jsonify({
                'therapists': [t.to_dict() for t in therapists]
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching therapists: {str(e)}")
            return jsonify({'error': 'Failed to fetch therapists'}), 500

    @bp.route('/therapist/<int:therapist_id>', methods=['GET'])
    def get_therapist(therapist_id):
        """Get therapist details"""
        try:
            therapist = User.query.filter_by(id=therapist_id, role='therapist').first()
            
            if not therapist:
                return jsonify({'error': 'Therapist not found'}), 404
                
            return jsonify(therapist.to_dict()), 200
            
        except Exception as e:
            logger.error(f"Error fetching therapist: {str(e)}")
            return jsonify({'error': 'Failed to fetch therapist details'}), 500

    @bp.route('/therapist/profile', methods=['GET', 'PUT'])
    @jwt_required()
    def therapist_profile():
        """Get or update therapist profile"""
        try:
            current_user_email = get_jwt_identity()
            therapist = User.query.filter_by(email=current_user_email, role='therapist').first()
            
            if not therapist:
                return jsonify({'error': 'Therapist not found'}), 404
            
            if request.method == 'GET':
                return jsonify(therapist.to_dict()), 200
            
            # Update profile
            data = request.get_json()
            updateable_fields = [
                'specialization', 'bio', 'years_of_experience', 'hourly_rate',
                'availability', 'profile_image', 'qualifications', 'languages'
            ]
            
            for field in updateable_fields:
                if field in data:
                    setattr(therapist, field, data[field])
            
            db.session.commit()
            return jsonify({
                'message': 'Profile updated successfully',
                'therapist': therapist.to_dict()
            }), 200
            
        except Exception as e:
            logger.error(f"Error managing therapist profile: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Failed to manage therapist profile'}), 500

# Initialize routes with the therapist blueprint
therapist_bp = Blueprint('therapist', __name__)
init_therapist_routes(therapist_bp) 