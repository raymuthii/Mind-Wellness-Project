from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # Retrieve current user ID from JWT and check for admin role
        current_user = get_jwt_identity()
        if not is_admin(current_user):
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def permission_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            # Check if the user has any of the required roles; admin bypasses all checks
            if not has_any_role(current_user, required_roles):
                return jsonify({'error': 'Permission denied'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def is_admin(user_id):
    """
    Check if the user has an admin role.
    For Mind Wellness, this can be used to enforce system-wide administrative privileges.
    """
    from models.user import User
    user = User.query.get(user_id)
    return user and user.role == 'admin'

def has_any_role(user_id, roles):
    """
    Check if the user has any of the specified roles.
    For Mind Wellness, admin users are granted all permissions.
    """
    from models.user import User
    user = User.query.get(user_id)
    if not user:
        return False
    return user.role in roles or user.role == 'admin'  # Admin has access to everything

def validate_required_fields(data, required_fields):
    """Utility function to validate required fields in request data"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    return True
