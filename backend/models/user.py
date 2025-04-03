"""User model"""
from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='patient')  # 'patient' or 'therapist'
    
    # Therapist specific fields
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    years_of_experience = db.Column(db.Integer)
    hourly_rate = db.Column(db.Float)
    availability = db.Column(db.JSON)  # Store availability as JSON
    profile_image = db.Column(db.String(255))  # URL to profile image
    qualifications = db.Column(db.JSON)  # Store qualifications as JSON array
    languages = db.Column(db.JSON)  # Store languages as JSON array
    is_verified = db.Column(db.Boolean, default=False)  # Verification status
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
        }
        
        if self.role == 'therapist':
            data.update({
                'specialization': self.specialization,
                'bio': self.bio,
                'years_of_experience': self.years_of_experience,
                'hourly_rate': self.hourly_rate,
                'availability': self.availability,
                'profile_image': self.profile_image,
                'qualifications': self.qualifications,
                'languages': self.languages,
                'is_verified': self.is_verified
            })
            
        return data 