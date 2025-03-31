from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from utils.decorators import admin_required
from services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__)

# Admin routes for managing all providers
@admin_bp.route('/providers', methods=['GET'])
@jwt_required()
@admin_required
def get_all_providers():
    """Get all providers including pending ones"""
    providers = AdminService.get_all_providers()
    return jsonify(providers), 200

@admin_bp.route('/providers/<int:provider_id>/approve', methods=['POST'])
@jwt_required()
@admin_required
def approve_provider(provider_id):
    """Approve a pending provider"""
    AdminService.approve_provider(provider_id)
    return jsonify({'message': 'Provider approved successfully'}), 200

@admin_bp.route('/providers/<int:provider_id>/reject', methods=['POST'])
@jwt_required()
@admin_required
def reject_provider(provider_id):
    """Reject a pending provider"""
    AdminService.reject_provider(provider_id)
    return jsonify({'message': 'Provider rejected'}), 200

# Admin routes for managing users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """Get all users"""
    users = AdminService.get_all_users()
    return jsonify(users), 200

@admin_bp.route('/users/<int:user_id>/block', methods=['POST'])
@jwt_required()
@admin_required
def block_user(user_id):
    """Block a user"""
    AdminService.block_user(user_id)
    return jsonify({'message': 'User blocked'}), 200
