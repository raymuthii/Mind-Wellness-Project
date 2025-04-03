"""Appointment model"""
from extensions import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    therapist = db.relationship('User', foreign_keys=[therapist_id], backref='appointments_as_therapist')
    patient = db.relationship('User', foreign_keys=[patient_id], backref='appointments_as_patient')
    
    def __repr__(self):
        return f'<Appointment {self.id}: {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'therapist_id': self.therapist_id,
            'patient_id': self.patient_id,
            'date': self.date.isoformat(),
            'duration': self.duration,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'patient': {
                'id': self.patient.id,
                'name': self.patient.name,
                'email': self.patient.email
            }
        } 