from app import db
from models.user import User
from backend.models.provider import Provider
from werkzeug.exceptions import NotFound, Forbidden

class AdminService:
    @staticmethod
    def get_pending_providers():
        """Get all pending provider applications"""
        return Provider.query.filter_by(status='pending').all()
    
    @staticmethod
    def approve_provider(provider_id):
        """Approve a provider application"""
        provider = Provider.query.get_or_404(provider_id)
        provider.status = 'active'
        db.session.commit()
        return provider
    
    @staticmethod
    def reject_provider(provider_id, reason=None):
        """Reject a provider application"""
        provider = Provider.query.get_or_404(provider_id)
        provider.status = 'rejected'
        provider.rejection_reason = reason
        db.session.commit()
        return provider
    
    @staticmethod
    def get_all_users():
        """Get all users in the system"""
        return User.query.all()
    
    @staticmethod
    def toggle_user_status(user_id):
        """Activate/deactivate a user"""
        user = User.query.get_or_404(user_id)
        user.is_active = not user.is_active
        db.session.commit()
        return user
    
    @staticmethod
    def change_user_role(user_id, new_role):
        """Change a user's role"""
        user = User.query.get_or_404(user_id)
        user.role = new_role
        db.session.commit()
        return user
