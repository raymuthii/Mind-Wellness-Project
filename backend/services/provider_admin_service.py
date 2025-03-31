from app import db
from backend.models.user import User
from backend.models.provider import Provider
from backend.models.success_story import SuccessStory
from backend.models.testimonial import Testimonial
from werkzeug.exceptions import NotFound, Forbidden

class ProviderAdminService:
    @staticmethod
    def get_provider_stats(provider_id, admin_id):
        """Get statistics for a provider"""
        provider = Provider.query.get_or_404(provider_id)
        if provider.admin_id != admin_id:
            raise Forbidden('You do not have permission to view this provider')
            
        return {
            'total_donations': provider.total_donations(),
            'donor_count': len(set(d.donor_id for d in provider.donations)),
            'success_story_count': len(provider.success_stories),
            'testimonial_count': len(provider.testimonials)
        }
    
    @staticmethod
    def update_provider_profile(provider_id, admin_id, data):
        """Update provider profile"""
        provider = Provider.query.get_or_404(provider_id)
        if provider.admin_id != admin_id:
            raise Forbidden('You do not have permission to update this provider')
            
        # Update allowed fields (note: 'phone' renamed to 'phone_number')
        for field in ['name', 'description', 'mission', 'phone_number', 'address']:
            if field in data:
                setattr(provider, field, data[field])
                
        db.session.commit()
        return provider
    
    @staticmethod
    def add_testimonial(provider_id, admin_id, data):
        """Add a new testimonial (formerly beneficiary)"""
        provider = Provider.query.get_or_404(provider_id)
        if provider.admin_id != admin_id:
            raise Forbidden('You do not have permission to add testimonials')
            
        testimonial = Testimonial(
            provider_id=provider_id,
            name=data['name'],
            description=data.get('description'),
            contact_info=data.get('contact_info')
        )
        
        db.session.add(testimonial)
        db.session.commit()
        return testimonial
    
    @staticmethod
    def create_success_story(provider_id, admin_id, data):
        """Create a new success story"""
        provider = Provider.query.get_or_404(provider_id)
        if provider.admin_id != admin_id:
            raise Forbidden('You do not have permission to create success stories')
            
        success_story = SuccessStory(
            provider_id=provider_id,
            author_id=admin_id,
            title=data['title'],
            content=data['content'],
            image_url=data.get('image_url'),
            status='draft'
        )
        
        db.session.add(success_story)
        db.session.commit()
        return success_story
    
    @staticmethod
    def publish_success_story(success_story_id, admin_id):
        """Publish a success story"""
        success_story = SuccessStory.query.get_or_404(success_story_id)
        if success_story.provider.admin_id != admin_id:
            raise Forbidden('You do not have permission to publish this success story')
            
        success_story.status = 'published'
        db.session.commit()
        return success_story
    
    @staticmethod
    def get_provider_donations(provider_id, admin_id):
        """Get all donations for a provider"""
        provider = Provider.query.get_or_404(provider_id)
        if provider.admin_id != admin_id:
            raise Forbidden('You do not have permission to view these donations')
            
        return provider.donations
    
    @staticmethod
    def get_donation_stats(provider_id, admin_id, period=None):
        """Get donation statistics for a provider"""
        provider = Provider.query.get_or_404(provider_id)
        if provider.admin_id != admin_id:
            raise Forbidden('You do not have permission to view these statistics')
            
        donations = provider.donations
        if period:
            # Add period filtering logic here (e.g., by date range)
            pass
            
        return {
            'total_amount': sum(d.amount for d in donations),
            'donation_count': len(donations),
            'recurring_count': len([d for d in donations if d.is_recurring]),
            'average_amount': sum(d.amount for d in donations) / len(donations) if donations else 0
        }
