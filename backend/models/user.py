from datetime import datetime, timezone, timedelta
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from backend.models import BaseModel, db
from backend.models.user import User

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    
    # Core fields
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False, server_default='user')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    profile_image = db.Column(db.String(255))
    
    # Authentication and security
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime)
    
    # Timestamps
    last_login_at = db.Column(db.DateTime)
    last_password_change = db.Column(db.DateTime)
    
    # Relationships
    donations = db.relationship(
        'Donation',
        back_populates='donor',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    managed_provider = db.relationship(
        'Provider',
        backref=db.backref('admin', lazy=True),
        lazy=True,
        uselist=False
    )
    success_stories = db.relationship(
        'SuccessStory',
        back_populates='author',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # Role constants
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLE_PROVIDER_ADMIN = 'provider_admin'
    
    # Configuration
    MAX_FAILED_ATTEMPTS = 10
    LOCKOUT_DURATION = 1  # minutes
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email:
            self.email = self.email.lower().strip()
        if self.name:
            self.name = self.name.strip()

    @hybrid_property
    def is_locked(self):
        if self.locked_until and self.locked_until > datetime.now(timezone.utc):
            return True
        return False

    def set_password(self, password):
        """Set hashed password."""
        self.password_hash = generate_password_hash(password)
        self.last_password_change = datetime.now(timezone.utc)
        self.failed_login_attempts = 0
        self.locked_until = None

    def check_password(self, password):
        """Check password and handle failed attempts."""
        if self.is_locked:
            return False
            
        is_valid = check_password_hash(self.password_hash, password)
        
        if is_valid:
            self.failed_login_attempts = 0
            self.locked_until = None
            self.last_login_at = datetime.now(timezone.utc)
        else:
            self.failed_login_attempts += 1
            if self.failed_login_attempts >= self.MAX_FAILED_ATTEMPTS:
                self.locked_until = datetime.now(timezone.utc) + timedelta(minutes=self.LOCKOUT_DURATION)
        
        return is_valid

    def get_id(self):
        """Return the user ID as a unicode string."""
        return str(self.id)

    @property
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == self.ROLE_ADMIN

    @property
    def is_provider_admin(self):
        """Check if user has provider admin role."""
        return self.role == self.ROLE_PROVIDER_ADMIN

    def can_manage_provider(self, provider_id):
        """Check if user can manage a specific provider."""
        return (self.is_admin or 
                (self.is_provider_admin and 
                 self.managed_provider and 
                 self.managed_provider.id == provider_id))

    def __repr__(self):
        return f'<User {self.email}>'

# SQLAlchemy event listeners
@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def normalize_email(mapper, connection, target):
    """Normalize email before save."""
    if target.email:
        target.email = target.email.lower().strip()

@event.listens_for(User, 'before_insert')
def set_default_role(mapper, connection, target):
    """Set default role if not provided."""
    if not target.role:
        target.role = User.ROLE_USER
