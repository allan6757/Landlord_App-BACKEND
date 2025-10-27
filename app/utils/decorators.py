# Role-Based Access Control (RBAC) Decorators
# These decorators protect routes and ensure only authorized users can access them

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.user import User, UserRole

def role_required(*allowed_roles):
    """
    Decorator to restrict access based on user roles
    Usage: @role_required(UserRole.ADMIN, UserRole.LANDLORD)
    
    Args:
        allowed_roles: One or more UserRole enum values
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Get current user ID from JWT token
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            # Check if user exists and has a profile
            if not user or not user.profile:
                return jsonify({'error': 'User not found or profile incomplete'}), 404
            
            # Check if user's role is in the allowed roles
            if user.profile.role not in allowed_roles:
                return jsonify({'error': 'Access denied. Insufficient permissions'}), 403
            
            # User has permission, proceed with the request
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    """
    Decorator to restrict access to admin users only
    Usage: @admin_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.profile:
            return jsonify({'error': 'User not found'}), 404
        
        if user.profile.role != UserRole.ADMIN:
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def landlord_required(fn):
    """
    Decorator to restrict access to landlord users only
    Usage: @landlord_required
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.profile:
            return jsonify({'error': 'User not found'}), 404
        
        if user.profile.role != UserRole.LANDLORD:
            return jsonify({'error': 'Landlord access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper
