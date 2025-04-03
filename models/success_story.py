from extensions import db

class SuccessStory(db.Model):
    __tablename__ = 'success_stories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='success_stories')
    
    def __repr__(self):
        return f'<SuccessStory {self.id}: {self.title}>' 