from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime, timezone

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base model class to add common columns to all models"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class Testimonial(BaseModel):
    __tablename__ = 'testimonials'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    contact_info = db.Column(db.String(255), nullable=False)
    status = db.Column(Enum('active', 'inactive', name='testimonial_status'), default='active', nullable=False)
    
    # Foreign Keys: linking the testimonial to a provider (formerly charity)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    
    # Relationships: update to reference the Provider model and testimonials relationship
    provider = db.relationship('Provider', back_populates='testimonials')
    inventory_received = db.relationship(
        'Inventory',
        back_populates='testimonial',
        cascade='all, delete-orphan'
    )
