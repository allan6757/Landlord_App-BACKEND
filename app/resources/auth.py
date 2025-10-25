from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User, UserProfile, UserRole
from app.schemas.user import UserSchema, LoginSchema

user_schema = UserSchema()
login_schema = LoginSchema()

class Register(Resource):
    def post(self):
        data = request.get_json()

        errors = user_schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        if User.query.filter_by(email=data['email']).first():
            return {'error': 'User with this email already exists'}, 400

        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        profile = UserProfile(user_id=user.id, role=UserRole.TENANT)
        db.session.add(profile)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        return {
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }, 201

class Login(Resource):
    def post(self):
        data = request.get_json()

        errors = login_schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        user = User.query.filter_by(email=data['email']).first()

        if user and user.check_password(data['password']):
            if not user.is_active:
                return {'error': 'Account is deactivated'}, 403

            user.update_last_login()
            db.session.commit()

            access_token = create_access_token(identity=user.id)

            return {
                'access_token': access_token,
                'user': user.to_dict()
            }, 200

        return {'error': 'Invalid email or password'}, 401

class Profile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return {'user': user.to_dict()}, 200