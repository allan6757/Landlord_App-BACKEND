from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db
from app.schemas.user import UserCreateSchema, UserSchema
from app.utils.email import send_welcome_email
from marshmallow import ValidationError

class Register(Resource):
    def post(self):
        schema = UserCreateSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already exists'}, 400
        
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data.get('phone'),
            role=data.get('role', 'tenant')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        send_welcome_email(user)
        
        return UserSchema().dump(user), 201

class Login(Resource):
    def post(self):
        data = request.json
        if not data or not data.get('email') or not data.get('password'):
            return {'error': 'Email and password required'}, 400
            
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']) and user.is_active:
            token = create_access_token(identity=user.id)
            return {
                'token': token,
                'user': UserSchema().dump(user)
            }, 200
        
        return {'error': 'Invalid credentials'}, 401

class Profile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return UserSchema().dump(user), 200
    
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        data = request.json
        updatable_fields = ['first_name', 'last_name', 'phone', 'profile_image']
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        db.session.commit()
        return UserSchema().dump(user), 200