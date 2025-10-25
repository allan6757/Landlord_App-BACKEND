from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Chat, db
from app.schemas.chat import ChatSchema, ChatCreateSchema

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/', methods=['GET'])
@jwt_required()
def get_messages():
    user_id = get_jwt_identity()
    messages = Chat.query.filter(
        (Chat.sender_id == user_id) | (Chat.receiver_id == user_id)
    ).order_by(Chat.created_at.desc()).all()
    return ChatSchema(many=True).dump(messages)

@chat_bp.route('/', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    schema = ChatCreateSchema()
    data = schema.load(request.json)
    
    message = Chat(**data, sender_id=user_id)
    db.session.add(message)
    db.session.commit()
    
    return ChatSchema().dump(message), 201