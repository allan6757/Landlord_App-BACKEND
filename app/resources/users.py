from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User, UserRole

class UserList(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)

        if current_user.profile.role != UserRole.ADMIN:
            return {'error': 'Admin access required'}, 403

        users = User.query.all()
        return {'users': [user.to_dict() for user in users]}, 200

class UserDetail(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get_or_404(current_user_id)
        user = User.query.get_or_404(user_id)

        if current_user.profile.role != UserRole.ADMIN and current_user.id != user.id:
            return {'error': 'Access denied'}, 403

        return {'user': user.to_dict()}, 200