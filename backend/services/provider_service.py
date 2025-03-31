from app import db
from backend.models.provider import Provider
from models.user import User
from werkzeug.exceptions import NotFound, Forbidden

class ProviderService:
    @staticmethod
    def get_all_providers():
        """Get all active providers"""
        return Provider.query.filter_by(status='active').all()
    
    @staticmethod
    def get_provider_by_id(provider_id):
        """Get provider by ID"""
        provider = Provider.query.get(provider_id)
        if not provider:
            raise NotFound('Provider not found')
        return provider

    @staticmethod
    def get_featured_providers():
        """Get featured providers"""
        return Provider.query.filter_by(
            status='active',
            featured=True
        ).all()

    @staticmethod
    def create_provider(data, admin_id):
        """Create a new provider"""
        # Check if admin exists
        admin = User.query.get(admin_id)
        if not admin:
            raise NotFound('Admin user not found')

        provider = Provider(
            name=data['name'],
            description=data['description'],
            email=data['email'],
            admin_id=admin_id,
            category=data['category'],
            mission=data.get('mission'),
            phone_number=data.get('phone'),  # Updated field: phone -> phone_number
            address=data.get('address'),
            logo_url=data.get('logo_url'),
            cover_image=data.get('cover_image'),
            status='pending'
        )
        
        if 'password' in data:
            provider.set_password(data['password'])

        db.session.add(provider)
        db.session.commit()
        return provider

    @staticmethod
    def update_provider(provider_id, data, user_id):
        """Update provider details"""
        provider = ProviderService.get_provider_by_id(provider_id)
        
        # Check if user has permission
        if provider.admin_id != user_id:
            raise Forbidden('You do not have permission to update this provider')

        # Update allowed fields
        allowed_fields = [
            'name', 'description', 'mission', 'phone', 
            'address', 'logo_url', 'cover_image', 'category'
        ]
        
        for field in allowed_fields:
            if field in data:
                # Update phone to phone_number for consistency
                if field == 'phone':
                    setattr(provider, 'phone_number', data[field])
                else:
                    setattr(provider, field, data[field])

        db.session.commit()
        return provider

    @staticmethod
    def update_provider_status(provider_id, status):
        """Update provider status (admin only)"""
        provider = ProviderService.get_provider_by_id(provider_id)
        provider.status = status
        db.session.commit()
        return provider

    @staticmethod
    def toggle_featured(provider_id):
        """Toggle provider featured status"""
        provider = ProviderService.get_provider_by_id(provider_id)
        provider.featured = not provider.featured
        db.session.commit()
        return provider

    @staticmethod
    def search_providers(query=None, category=None):
        """Search providers by name or category"""
        providers = Provider.query.filter_by(status='active')
        
        if query:
            providers = providers.filter(Provider.name.ilike(f'%{query}%'))
        if category:
            providers = providers.filter_by(category=category)
            
        return providers.all()

    @staticmethod
    def get_provider_stats(provider_id):
        """Get provider statistics"""
        provider = ProviderService.get_provider_by_id(provider_id)
        return {
            'total_donations': provider.total_donations(),
            'donor_count': len(set(d.donor_id for d in provider.donations)),
            'success_story_count': len(provider.success_stories),
            'testimonial_count': len(provider.testimonials)
        }
