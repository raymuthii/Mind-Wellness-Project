"""Appointment endpoints"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime

from models import User, Appointment, db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_appointment_routes(bp):
    @bp.route('/appointments', methods=['GET'])
    @jwt_required()
    def get_appointments():
        """Get appointments for the current user"""
        try:
            current_user_email = get_jwt_identity()
            user = User.query.filter_by(email=current_user_email).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Get appointments based on user role
            if user.role == 'therapist':
                appointments = Appointment.query.filter_by(therapist_id=user.id).all()
            else:
                appointments = Appointment.query.filter_by(patient_id=user.id).all()
            
            return jsonify({
                'appointments': [app.to_dict() for app in appointments]
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching appointments: {str(e)}")
            return jsonify({'error': 'Failed to fetch appointments'}), 500

    @bp.route('/appointments', methods=['POST'])
    @jwt_required()
    def create_appointment():
        """Create a new appointment"""
        try:
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
            return jsonify({'error': 'Failed to create appointment'}), 500

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