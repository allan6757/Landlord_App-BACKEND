from flask_restful import Resource
from flask import request, current_app, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.schemas.user import UserCreateSchema, UserSchema
from marshmallow import ValidationError

class Register(Resource):
    def post(self):
        try:
            # Validate input data
            if not request.json:
                return {'error': 'No JSON data provided'}, 400
            
            schema = UserCreateSchema()
            data = schema.load(request.json)
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return {'error': 'Email already exists'}, 400
            
            # Create new user
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
            
            current_app.logger.info(f"New user registered: {user.email}")
            
            return {
                'message': 'User registered successfully',
                'user': UserSchema().dump(user)
            }, 201
            
        except ValidationError as err:
            current_app.logger.error(f"Registration validation error: {err.messages}")
            return {'errors': err.messages}, 400
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            return {'error': 'Registration failed. Please try again.'}, 500

class Login(Resource):
    def post(self):
        try:
            # Validate input
            if not request.json:
                return {'error': 'No JSON data provided'}, 400
            
            data = request.json
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return {'error': 'Email and password are required'}, 400
            
            # Find user
            user = User.query.filter_by(email=email).first()
            
            if not user:
                current_app.logger.warning(f"Login attempt with non-existent email: {email}")
                return {'error': 'Invalid email or password'}, 401
            
            if not user.is_active:
                return {'error': 'Account is deactivated'}, 401
            
            # Check password
            if not user.check_password(password):
                current_app.logger.warning(f"Failed login attempt for: {email}")
                return {'error': 'Invalid email or password'}, 401
            
            # Generate token
            token = create_access_token(identity=user.id)
            
            current_app.logger.info(f"Successful login: {user.email}")
            
            return {
                'message': 'Login successful',
                'token': token,
                'user': UserSchema().dump(user)
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            return {'error': 'Login failed. Please try again.'}, 500

class Profile(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return {
                'user': UserSchema().dump(user)
            }, 200
            
        except Exception as e:
            current_app.logger.error(f"Profile get error: {str(e)}")
            return {'error': 'Failed to get profile'}, 500
    
    @jwt_required()
    def put(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            data = request.json or {}
            updatable_fields = ['first_name', 'last_name', 'phone', 'profile_image']
            
            for field in updatable_fields:
                if field in data:
                    setattr(user, field, data[field])
            
            db.session.commit()
            
            return {
                'message': 'Profile updated successfully',
                'user': UserSchema().dump(user)
            }, 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Profile update error: {str(e)}")
            return {'error': 'Failed to update profile'}, 500