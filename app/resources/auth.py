from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db
from app.schemas.user import UserCreateSchema, UserSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    schema = UserCreateSchema()
    data = schema.load(request.json)
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(**data)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return UserSchema().dump(user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token, 'user': UserSchema().dump(user)})
    
    return jsonify({'error': 'Invalid credentials'}), 401