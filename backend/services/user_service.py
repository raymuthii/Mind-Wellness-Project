from typing import Optional, List
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

from models.user import User
from extensions import db
from utils import validate_required_fields

class UserService:
    @staticmethod
    def create_user(data: dict) -> User:
        """
        Create a new user
        """
        # Validate required fields
        required_fields = ['email', 'password', 'name']
        validate_required_fields(data, required_fields)
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            raise ValueError('Email already registered')
            
        # Create new user
        user = User(
            email=data['email'],
            name=data['name'],
            password=generate_password_hash(data['password']),
            role=data.get('role', 'user')  # Default role is 'user'
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user

    @staticmethod
    def authenticate_user(email: str, password: str) -> dict:
        """
        Authenticate user and return JWT token
        """
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            raise ValueError('Invalid email or password')
            
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=1)
        )
        
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role
            }
        }

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Get user by ID
        """
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id: int, data: dict, current_user_id: int) -> User:
        """
        Update user details
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
            
        # Only allow users to update their own profile unless they're admin
        if current_user_id != user_id:
            current_user = User.query.get(current_user_id)
            if not current_user or current_user.role != 'admin':
                raise ValueError('Permission denied')
        
        # Update allowed fields
        allowed_fields = ['name', 'email']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
                
        # Handle password update separately
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
            
        db.session.commit()
        return user

    @staticmethod
    def update_user_role(user_id: int, new_role: str, admin_user_id: int) -> User:
        """
        Update user role (admin only)
        """
        # Verify admin
        admin_user = User.query.get(admin_user_id)
        if not admin_user or admin_user.role != 'admin':
            raise ValueError('Admin access required')
            
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
            
        valid_roles = ['user', 'admin', 'provider_admin']  # Updated valid role from charity_admin to provider_admin
        if new_role not in valid_roles:
            raise ValueError(f'Invalid role. Must be one of: {", ".join(valid_roles)}')
            
        user.role = new_role
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id: int, admin_user_id: int) -> None:
        """
        Delete user (admin only)
        """
        # Verify admin
        admin_user = User.query.get(admin_user_id)
        if not admin_user or admin_user.role != 'admin':
            raise ValueError('Admin access required')
            
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
            
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def get_users(page: int = 1, per_page: int = 20) -> List[User]:
        """
        Get paginated list of users
        """
        return User.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def search_users(query: str, page: int = 1, per_page: int = 20) -> List[User]:
        """
        Search users by email or name
        """
        return User.query.filter(
            (User.email.ilike(f'%{query}%')) |
            (User.name.ilike(f'%{query}%'))
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
