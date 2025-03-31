from app import db
from backend.models.testimonial import BaseModel  # Ensure BaseModel is imported from the updated file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import func

class Provider(BaseModel):
    """
    Provider model for mental health organizations that receive donations
    and manage patient testimonials and success stories.
    """
    __tablename__ = 'providers'
    
    # Basic Information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    mission = db.Column(db.Text)
    
    # Media/Assets
    logo_url = db.Column(db.String(255))
    cover_image = db.Column(db.String(255))
    
    # Contact Information
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(255))
    
    # Authentication
    password_hash = db.Column(db.String(10000), nullable=False)
    
    # Classification
    category = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # pending, active, inactive
    featured = db.Column(db.Boolean, default=False)
    
    # Foreign Keys
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    donations = db.relationship('Donation', back_populates='provider', lazy=True)
    testimonials = db.relationship('Testimonial', back_populates='provider', lazy=True)
    success_stories = db.relationship('SuccessStory', back_populates='provider', lazy=True)
    inventory_items = db.relationship('Inventory', back_populates='provider', lazy=True)

    def __init__(self, **kwargs):
        super(Provider, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])

    def __repr__(self):
        return f'<Provider {self.name}>'

    @property
    def is_active(self):
        """Check if provider is active"""
        return self.status == 'active'

    def set_password(self, password):
        """Set hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def total_donations(self):
        """Calculate total donations received"""
        return sum(donation.amount for donation in self.donations if donation.status == 'completed')

    def donor_count(self):
        """Get unique donor count"""
        return len(set(donation.donor_id for donation in self.donations if donation.status == 'completed'))

    def recent_donations(self, limit=5):
        """Get recent donations"""
        return sorted(
            [d for d in self.donations if d.status == 'completed'],
            key=lambda x: x.created_at,
            reverse=True
        )[:limit]

    def activate(self):
        """Activate provider"""
        self.status = 'active'
        return self

    def deactivate(self):
        """Deactivate provider"""
        self.status = 'inactive'
        return self

    def toggle_featured(self):
        """Toggle featured status"""
        self.featured = not self.featured
        return self

    @classmethod
    def get_featured(cls):
        """Get all featured providers"""
        return cls.query.filter_by(featured=True, status='active').all()

    @classmethod
    def get_by_category(cls, category):
        """Get providers by category"""
        return cls.query.filter_by(category=category, status='active').all()

    def to_dict(self):
        """Convert provider to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'mission': self.mission,
            'logo_url': self.logo_url,
            'cover_image': self.cover_image,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'category': self.category,
            'status': self.status,
            'featured': self.featured,
            'admin_id': self.admin_id,
            'total_donations': self.total_donations(),
            'donor_count': self.donor_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
