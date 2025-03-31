from datetime import datetime
from backend.extensions import db

class BaseModel(db.Model):
    """Base model class for the Mind Wellness platform, including common fields and methods."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
