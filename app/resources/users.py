from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db
from app.schemas.user import UserSchema
from app.utils.cloudinary import upload_image

class UserList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        # Only admins can list all users
        if user.role != 'admin':
            return {'error': 'Admin access required'}, 403
            
        users = User.query.all()
        return {'users': [user.to_dict() for user in users]}, 200

class UserDetail(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)
        
        # Users can only view their own profile unless they're admin
        if current_user.role != 'admin' and current_user_id != user_id:
            return {'error': 'Access denied'}, 403
            
        user = User.query.get_or_404(user_id)
        return {'user': user.to_dict()}, 200

class UserProfileImage(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if 'image' not in request.files:
            return {'error': 'No image file provided'}, 400
        
        file = request.files['image']
        if file.filename == '':
            return {'error': 'No file selected'}, 400
            
        result = upload_image(file, folder=f"users/{user_id}")
        
        if 'error' in result:
            return {'error': result['error']}, 400
        
        user.profile_image = result['url']
        db.session.commit()
        
        return {'profile_image': result['url']}, 200