from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models import User

def landlord_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'landlord':
            return {'error': 'Landlord access required'}, 403
        return f(*args, **kwargs)
    return decorated_function

def tenant_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'tenant':
            return {'error': 'Tenant access required'}, 403
        return f(*args, **kwargs)
    return decorated_function