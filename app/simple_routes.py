from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app import db

class SimpleRegister(Resource):
    def post(self):
        try:
            from app.models import User
            
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', 'User')
            last_name = data.get('last_name', 'Name')
            role = data.get('role', 'tenant')
            
            if not email or not password:
                return {'error': 'Email and password required'}, 400
            
            # Check if user exists
            if User.query.filter_by(email=email).first():
                return {'error': 'User already exists'}, 409
            
            # Create user
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Create token
            token = create_access_token(identity=user.id)
            
            return {
                'success': True,
                'token': token,
                'user': user.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class SimpleLogin(Resource):
    def post(self):
        try:
            from app.models import User
            
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return {'error': 'Email and password required'}, 400
            
            # Find user
            user = User.query.filter_by(email=email).first()
            
            if not user or not user.check_password(password):
                return {'error': 'Invalid credentials'}, 401
            
            # Create token
            token = create_access_token(identity=user.id)
            
            return {
                'success': True,
                'token': token,
                'user': user.to_dict()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500