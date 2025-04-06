"""Appointment endpoints"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import logging
from datetime import datetime
import traceback

from backend.models import User, Appointment, db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_appointment_routes(bp):
    @bp.route('/appointments', methods=['GET', 'OPTIONS'])
    def get_appointments():
        """Get appointments for the current user"""
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'ok'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3001')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200

        try:
            # Verify JWT token
            verify_jwt_in_request()
            
            # Get current user
            current_user_email = get_jwt_identity()
            logger.info(f"Processing request for user: {current_user_email}")
            
            user = User.query.filter_by(email=current_user_email).first()
            if not user:
                logger.error(f"User not found: {current_user_email}")
                return jsonify({'error': 'User not found'}), 404
            
            logger.info(f"User role: {user.role}")
            
            # Get appointments based on user role
            if user.role == 'therapist':
                appointments = Appointment.query.filter_by(therapist_id=user.id).all()
                logger.info(f"Found {len(appointments)} appointments for therapist {user.id}")
            else:
                appointments = Appointment.query.filter_by(patient_id=user.id).all()
                logger.info(f"Found {len(appointments)} appointments for patient {user.id}")
            
            # Convert appointments to dict
            appointment_list = []
            for app in appointments:
                try:
                    appointment_dict = app.to_dict()
                    appointment_list.append(appointment_dict)
                except Exception as e:
                    logger.error(f"Error converting appointment to dict: {str(e)}")
                    logger.error(traceback.format_exc())
            
            response = jsonify({
                'appointments': appointment_list
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3001')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200
            
        except Exception as e:
            logger.error(f"Error fetching appointments: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'error': 'Failed to fetch appointments', 'details': str(e)}), 500

    @bp.route('/appointments', methods=['POST', 'OPTIONS'])
    def create_appointment():
        """Create a new appointment"""
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'ok'})
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3001')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response, 200

        try:
            # Verify JWT token
            verify_jwt_in_request()
            
            current_user_email = get_jwt_identity()
            patient = User.query.filter_by(email=current_user_email).first()
            
            if not patient or patient.role != 'patient':
                return jsonify({'error': 'Only patients can create appointments'}), 403
            
            data = request.get_json()
            required_fields = ['therapist_id', 'date', 'duration']
            
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400
            
            # Check if therapist exists
            therapist = User.query.filter_by(id=data['therapist_id'], role='therapist').first()
            if not therapist:
                return jsonify({'error': 'Therapist not found'}), 404
            
            # Create appointment
            appointment = Appointment(
                therapist_id=data['therapist_id'],
                patient_id=patient.id,
                date=datetime.fromisoformat(data['date']),
                duration=data['duration'],
                notes=data.get('notes')
            )
            
            db.session.add(appointment)
            db.session.commit()
            
            return jsonify({
                'message': 'Appointment created successfully',
                'appointment': appointment.to_dict()
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating appointment: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Failed to create appointment', 'details': str(e)}), 500

    @bp.route('/appointments/<int:appointment_id>/status', methods=['PUT'])
    @jwt_required()
    def update_appointment_status(appointment_id):
        """Update appointment status (accept/decline)"""
        try:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            
            if not user or user.role != 'therapist':
                return jsonify({'error': 'Only therapists can update appointment status'}), 403
            
            appointment = Appointment.query.filter_by(
                id=appointment_id,
                therapist_id=user.id
            ).first()
            
            if not appointment:
                return jsonify({'error': 'Appointment not found'}), 404
            
            data = request.get_json()
            if 'status' not in data or data['status'] not in ['accepted', 'declined']:
                return jsonify({'error': 'Invalid status'}), 400
            
            appointment.status = data['status']
            db.session.commit()
            
            return jsonify({
                'message': f'Appointment {data["status"]} successfully',
                'appointment': appointment.to_dict()
            }), 200
            
        except Exception as e:
            logger.error(f"Error updating appointment status: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Failed to update appointment status'}), 500

# Initialize routes with the appointment blueprint
appointment_bp = Blueprint('appointment', __name__)
init_appointment_routes(appointment_bp) 