from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import provider_admin_required
from services.provider_admin_service import ProviderAdminService

provider_admin_bp = Blueprint('provider_admin', __name__)

@provider_admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@provider_admin_required
def get_dashboard():
    """Get provider admin dashboard data"""
    admin_id = get_jwt_identity()
    dashboard_data = ProviderAdminService.get_dashboard_data(admin_id)
    return jsonify(dashboard_data), 200

@provider_admin_bp.route('/testimonials', methods=['POST'])
@jwt_required()
@provider_admin_required
def add_testimonial():
    """Add a new patient testimonial"""
    admin_id = get_jwt_identity()
    data = request.get_json()
    testimonial = ProviderAdminService.add_testimonial(admin_id, data)
    return jsonify(testimonial), 201

@provider_admin_bp.route('/success-stories', methods=['POST'])
@jwt_required()
@provider_admin_required
def create_success_story():
    """Create a new success story"""
    admin_id = get_jwt_identity()
    data = request.get_json()
    success_story = ProviderAdminService.create_success_story(admin_id, data)
    return jsonify(success_story), 201

@provider_admin_bp.route('/donations', methods=['GET'])
@jwt_required()
@provider_admin_required
def get_donations():
    """Get all donations for the provider"""
    admin_id = get_jwt_identity()
    donations = ProviderAdminService.get_donations(admin_id)
    return jsonify(donations), 200

@provider_admin_bp.route('/inventory', methods=['POST'])
@jwt_required()
@provider_admin_required
def add_inventory():
    """Add new inventory items"""
    admin_id = get_jwt_identity()
    data = request.get_json()
    inventory = ProviderAdminService.add_inventory(admin_id, data)
    return jsonify(inventory), 201
