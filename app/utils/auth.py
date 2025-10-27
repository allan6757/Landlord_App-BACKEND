from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def get_current_user():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except:
        return None

def require_roles(roles):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            if not current_user or not current_user.profile or current_user.profile.role.value not in roles:
                return {'error': 'Insufficient permissions'}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator