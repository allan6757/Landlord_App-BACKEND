from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.utils.errors import AuthError, create_error_response, create_success_response

class Register(Resource):
    def post(self):
        try:
            from app import db
            from app.models import User
            from app.schemas.user import UserCreateSchema, UserSchema
            
            if not request.json:
                return create_error_response(
                    "Request body is required", 
                    AuthError.VALIDATION_ERROR, 
                    400
                )
            
            schema = UserCreateSchema()
            data = schema.load(request.json)
            
            # Check if user already exists
            if User.query.filter_by(email=data['email']).first():
                return create_error_response(
                    "An account with this email already exists", 
                    AuthError.EMAIL_EXISTS, 
                    409
                )
            
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
            
            # Generate token
            token = create_access_token(identity=user.id)
            
            return create_success_response({
                'token': token,
                'user': UserSchema().dump(user)
            }, "Account created successfully", 201)
            
        except ValidationError as err:
            return create_error_response(
                "Please check your input and try again", 
                AuthError.VALIDATION_ERROR, 
                400
            )
        except Exception as e:
            current_app.logger.error(f"Registration error: {str(e)}")
            db.session.rollback()
            return create_error_response(
                "Unable to create account. Please try again later", 
                AuthError.SERVER_ERROR, 
                500
            )

class Login(Resource):
    def post(self):
        try:
            from app import db
            from app.models import User
            from app.schemas.user import UserSchema
            
            if not request.json:
                return create_error_response(
                    "Email and password are required", 
                    AuthError.VALIDATION_ERROR, 
                    400
                )
            
            data = request.json
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            if not email or not password:
                return create_error_response(
                    "Email and password are required", 
                    AuthError.VALIDATION_ERROR, 
                    400
                )
            
            # Find user
            user = User.query.filter_by(email=email).first()
            
            if not user or not user.check_password(password):
                return create_error_response(
                    "Invalid email or password", 
                    AuthError.INVALID_CREDENTIALS, 
                    401
                )
            
            if not user.is_active:
                return create_error_response(
                    "Your account has been disabled", 
                    AuthError.ACCOUNT_DISABLED, 
                    403
                )
            
            # Generate token
            token = create_access_token(identity=user.id)
            
            return create_success_response({
                'token': token,
                'user': UserSchema().dump(user)
            }, "Login successful")
            
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            return create_error_response(
                "Unable to sign in. Please try again later", 
                AuthError.SERVER_ERROR, 
                500
            )

class Profile(Resource):
    @jwt_required()
    def get(self):
        try:
            from app.models import User
            from app.schemas.user import UserSchema
            
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return create_error_response(
                    "User not found", 
                    AuthError.INVALID_CREDENTIALS, 
                    404
                )
            
            return create_success_response({
                'user': UserSchema().dump(user)
            })
            
        except Exception as e:
            current_app.logger.error(f"Profile error: {str(e)}")
            return create_error_response(
                "Unable to load profile", 
                AuthError.SERVER_ERROR, 
                500
            )
    
    @jwt_required()
    def put(self):
        try:
            from app import db
            from app.models import User
            from app.schemas.user import UserSchema
            
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return create_error_response(
                    "User not found", 
                    AuthError.INVALID_CREDENTIALS, 
                    404
                )
            
            data = request.json or {}
            updatable_fields = ['first_name', 'last_name', 'phone', 'profile_image']
            
            for field in updatable_fields:
                if field in data:
                    setattr(user, field, data[field])
            
            db.session.commit()
            
            return create_success_response({
                'user': UserSchema().dump(user)
            }, "Profile updated successfully")
            
        except Exception as e:
            current_app.logger.error(f"Profile update error: {str(e)}")
            db.session.rollback()
            return create_error_response(
                "Unable to update profile", 
                AuthError.SERVER_ERROR, 
                500
            )