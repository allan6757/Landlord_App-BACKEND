from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.chat import Conversation, Message
from app.models.user import User
from app.models.property import Property
from app.schemas.chat import ConversationSchema, MessageSchema, ConversationCreateSchema, MessageCreateSchema

conversation_schema = ConversationSchema()
message_schema = MessageSchema()
conversation_create_schema = ConversationCreateSchema()
message_create_schema = MessageCreateSchema()

class ConversationList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        conversations = Conversation.query.filter(
            (Conversation.initiator_id == user.id) | 
            (Conversation.participant_id == user.id)
        ).order_by(Conversation.last_message_at.desc()).all()

        return {'conversations': [conv.to_dict() for conv in conversations]}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        data = request.get_json()
        errors = conversation_create_schema.validate(data)
        if errors:
            return {'errors': errors}, 400
        
        # Check if conversation already exists
        existing_conv = Conversation.query.filter(
            ((Conversation.initiator_id == user.id) & (Conversation.participant_id == data['participant_id'])) |
            ((Conversation.initiator_id == data['participant_id']) & (Conversation.participant_id == user.id))
        ).first()
        
        if existing_conv:
            return {'conversation': existing_conv.to_dict()}, 200
        
        conversation = Conversation(
            initiator_id=user.id,
            participant_id=data['participant_id'],
            property_id=data.get('property_id'),
            title=data.get('title')
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return {'conversation': conversation.to_dict()}, 201
class ConversationDetail(Resource):
    @jwt_required()
    def get(self, conversation_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        conversation = Conversation.query.get_or_404(conversation_id)

        if conversation.initiator_id != user.id and conversation.participant_id != user.id:
            return {'error': 'Access denied'}, 403
        
        # Mark all messages as read for current user
        unread_messages = Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user.id,
            Message.is_read == False
        ).all()
        
        for message in unread_messages:
            message.mark_as_read()
        
        return {'conversation': conversation.to_dict()}, 200

    @jwt_required()
    def delete(self, conversation_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        conversation = Conversation.query.get_or_404(conversation_id)
        
        if conversation.initiator_id != user.id and conversation.participant_id != user.id:
            return {'error': 'Access denied'}, 403
        
        db.session.delete(conversation)
        db.session.commit()
        
        return {'message': 'Conversation deleted successfully'}, 200
class MessageList(Resource):
    @jwt_required()
    def get(self, conversation_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        conversation = Conversation.query.get_or_404(conversation_id)

        if conversation.initiator_id != user.id and conversation.participant_id != user.id:
            return {'error': 'Access denied'}, 403

        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at.asc()).all()

        return {'messages': [msg.to_dict() for msg in messages]}, 200

    @jwt_required()
    def post(self, conversation_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        conversation = Conversation.query.get_or_404(conversation_id)

        if conversation.initiator_id != user.id and conversation.participant_id != user.id:
            return {'error': 'Access denied'}, 403

        data = request.get_json()
        errors = message_create_schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        message = Message(
            content=data['content'],
            conversation_id=conversation_id,
            sender_id=user.id
        )

        db.session.add(message)
        conversation.update_last_message(data['content'])
        db.session.commit()

        return {'message': message.to_dict()}, 201