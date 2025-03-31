from datetime import datetime
from app import db
from .testimonial import BaseModel

class SuccessStory(BaseModel):
    """
    SuccessStory model for mental health impact stories and updates.
    Represents stories highlighting the success and impact of mental health providers.
    """
    __tablename__ = 'success_stories'
    
    # Status Constants
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'
    
    # Column Definitions
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default=STATUS_DRAFT)
    featured = db.Column(db.Boolean, default=False)
    
    # Engagement Metrics
    view_count = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    
    # Publishing Info
    published_at = db.Column(db.DateTime)
    
    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    
    # Relationships
    author = db.relationship('User', back_populates='success_stories')
    provider = db.relationship('Provider', back_populates='success_stories')

    def __repr__(self):
        return f'<SuccessStory {self.title}>'

    @property
    def is_published(self):
        """Check if success story is published"""
        return self.status == self.STATUS_PUBLISHED

    @property
    def is_draft(self):
        """Check if success story is draft"""
        return self.status == self.STATUS_DRAFT

    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes"""
        words_per_minute = 200
        word_count = len(self.content.split())
        minutes = word_count / words_per_minute
        return max(1, round(minutes))

    def publish(self):
        """Publish the success story"""
        self.status = self.STATUS_PUBLISHED
        self.published_at = datetime.utcnow()
        return self

    def archive(self):
        """Archive the success story"""
        self.status = self.STATUS_ARCHIVED
        return self

    def increment_view(self):
        """Increment view count"""
        self.view_count += 1
        return self

    def increment_likes(self):
        """Increment likes count"""
        self.likes += 1
        return self

    def increment_shares(self):
        """Increment shares count"""
        self.shares += 1
        return self

    def toggle_featured(self):
        """Toggle featured status"""
        self.featured = not self.featured
        return self

    @classmethod
    def get_featured(cls):
        """Get all featured success stories"""
        return cls.query.filter_by(
            featured=True, 
            status=cls.STATUS_PUBLISHED
        ).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_provider(cls, provider_id):
        """Get all published success stories for a provider"""
        return cls.query.filter_by(
            provider_id=provider_id,
            status=cls.STATUS_PUBLISHED
        ).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_trending(cls, limit=5):
        """Get trending success stories based on engagement"""
        return cls.query.filter_by(
            status=cls.STATUS_PUBLISHED
        ).order_by(
            (cls.view_count + cls.likes + cls.shares).desc()
        ).limit(limit).all()

    def to_dict(self):
        """Convert success story to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'image_url': self.image_url,
            'status': self.status,
            'featured': self.featured,
            'view_count': self.view_count,
            'likes': self.likes,
            'shares': self.shares,
            'reading_time': self.reading_time,
            'author_id': self.author_id,
            'provider_id': self.provider_id,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
