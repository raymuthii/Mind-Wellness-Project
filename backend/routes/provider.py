from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.provider import Provider
from schemas.provider import ProviderSchema
from services.provider_service import ProviderService
from ..utils.decorators import admin_required
from app import db

provider_bp = Blueprint('provider', __name__)
provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)

@provider_bp.route('/', methods=['GET'])
def get_providers():
    """Get all active providers"""
    try:
        providers = Provider.query.filter_by(status='active').all()
        return jsonify(providers_schema.dump(providers)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@provider_bp.route('/<int:id>', methods=['GET'])
def get_provider(id):
    """Get a specific provider by ID"""
    try:
        provider = Provider.query.get_or_404(id)
        return jsonify(provider_schema.dump(provider)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@provider_bp.route('/featured', methods=['GET'])
def get_featured_providers():
    """Get featured providers"""
    try:
        featured = Provider.query.filter_by(
            status='active', 
            featured=True
        ).all()
        return jsonify(providers_schema.dump(featured)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@provider_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_provider():
    """Apply for a new provider account"""
    try:
        data = request.get_json()
        data['admin_id'] = get_jwt_identity()
        data['status'] = 'pending'  # All new applications start as pending

        # Validate required fields
        required_fields = ['name', 'description', 'email', 'category']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        provider = provider_schema.load(data)
        provider.set_password(data['password'])
        
        db.session.add(provider)
        db.session.commit()

        return jsonify({
            'message': 'Provider application submitted successfully',
            'provider': provider_schema.dump(provider)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@provider_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_provider(id):
    """Update provider details"""
    try:
        provider = Provider.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if user is provider admin or system admin
        if provider.admin_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'name', 'description', 'mission', 'logo_url', 
            'cover_image', 'phone_number', 'address', 'category'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(provider, field, data[field])
        
        db.session.commit()
        return jsonify(provider_schema.dump(provider)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@provider_bp.route('/<int:id>/status', methods=['PATCH'])
@jwt_required()
@admin_required
def update_provider_status(id):
    """Update provider status (Admin only)"""
    try:
        provider = Provider.query.get_or_404(id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
            
        if data['status'] not in ['pending', 'active', 'inactive']:
            return jsonify({'error': 'Invalid status'}), 400
        
        provider.status = data['status']
        db.session.commit()
        
        return jsonify({
            'message': f'Provider status updated to {data["status"]}',
            'provider': provider_schema.dump(provider)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@provider_bp.route('/<int:id>/featured', methods=['PATCH'])
@jwt_required()
@admin_required
def toggle_featured(id):
    """Toggle provider featured status (Admin only)"""
    try:
        provider = Provider.query.get_or_404(id)
        provider.featured = not provider.featured
        db.session.commit()
        
        return jsonify({
            'message': 'Provider featured status updated',
            'featured': provider.featured,
            'provider': provider_schema.dump(provider)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@provider_bp.route('/search', methods=['GET'])
def search_providers():
    """Search providers by name or category"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category', '')
        
        providers = Provider.query.filter_by(status='active')
        
        if query:
            providers = providers.filter(Provider.name.ilike(f'%{query}%'))
        if category:
            providers = providers.filter_by(category=category)
            
        return jsonify(providers_schema.dump(providers.all())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
