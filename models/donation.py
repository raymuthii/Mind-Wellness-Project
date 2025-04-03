from extensions import db

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    transaction_id = db.Column(db.String(100))
    
    # Relationships
    user = db.relationship('User', backref='donations')
    
    def __repr__(self):
        return f'<Donation {self.id}: {self.amount}>' 