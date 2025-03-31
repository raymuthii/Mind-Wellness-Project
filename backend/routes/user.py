from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from schemas.user import UserSchema
from ..app import db

user_bp = Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        return jsonify(user_schema.dump(user)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()

        # Only update allowed fields
        allowed_fields = ['name', 'email', 'profile_image']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user_schema.dump(user)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@user_bp.route('/donations', methods=['GET'])
@jwt_required()
def get_user_donations():
    """Get current user's donations"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        return jsonify({
            'donations': [
                {
                    'id': d.id,
                    'amount': float(d.amount),
                    'provider_name': d.provider.name,  # Updated: provider instead of charity
                    'date': d.created_at.isoformat(),
                    'status': d.status
                } for d in user.donations
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/stories', methods=['GET'])
@jwt_required()
def get_user_success_stories():
    """Get success stories written by current user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        return jsonify({
            'success_stories': [
                {
                    'id': s.id,
                    'title': s.title,
                    'provider_name': s.provider.name,  # Updated: provider instead of charity
                    'date': s.created_at.isoformat(),
                    'status': s.status
                } for s in user.success_stories  # Updated: use success_stories relationship
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user's password"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()

        if not user.check_password(data.get('current_password')):
            return jsonify({'error': 'Current password is incorrect'}), 400

        if data.get('new_password') != data.get('confirm_password'):
            return jsonify({'error': 'New passwords do not match'}), 400

        user.set_password(data['new_password'])
        db.session.commit()

        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@user_bp.route('/deactivate', methods=['POST'])
@jwt_required()
def deactivate_account():
    """Deactivate user account"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        
        user.is_active = False
        db.session.commit()

        return jsonify({'message': 'Account deactivated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Admin only routes
@user_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        users = User.query.all()
        return jsonify(users_schema.dump(users)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
