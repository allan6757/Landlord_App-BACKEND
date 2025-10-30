# ============================================================================
# CHAT ENDPOINTS - Real-time Messaging Between Landlords and Tenants
# ============================================================================
# REST API endpoints for chat conversations and messages
#
# ENDPOINTS:
# GET /api/conversations - List all conversations for current user
# POST /api/conversations - Create new conversation
# GET /api/conversations/<id> - Get conversation details
# DELETE /api/conversations/<id> - Delete conversation
# GET /api/conversations/<id>/messages - Get all messages in conversation
# POST /api/conversations/<id>/messages - Send new message
#
# CONVERSATION STRUCTURE:
# {
#   "id": 1,
#   "initiator_id": 2,      // sender_id
#   "participant_id": 3,    // receiver_id
#   "property_id": 1,
#   "last_message": "Hello",
#   "last_message_at": "2024-01-15T10:30:00"
# }
#
# MESSAGE STRUCTURE:
# {
#   "id": 1,
#   "sender_id": 2,
#   "content": "Hello, is the property available?",
#   "timestamp": "2024-01-15T10:30:00",
#   "is_read": false
# }
#
# CREATE CONVERSATION REQUEST:
# {
#   "participant_id": 3,  // User to chat with
#   "property_id": 1      // Optional: Related property
# }
#
# SEND MESSAGE REQUEST:
# {
#   "content": "Hello, is the property available?"
# }
#
# REAL-TIME UPDATES:
# Use Socket.IO for instant message delivery (see app/sockets/__init__.py)
# ============================================================================

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
    """Conversation list endpoint - Get all conversations or create new one"""
    @jwt_required()  # Requires JWT token in Authorization header
    def get(self):
        """Get all conversations for current user
        Returns conversations where user is either initiator or participant
        """
        user_id = get_jwt_identity()  # Extract user ID from JWT token
        user = User.query.get_or_404(user_id)

        # Get conversations where user is involved (as initiator or participant)
        conversations = Conversation.query.filter(
            (Conversation.initiator_id == user.id) | 
            (Conversation.participant_id == user.id)
        ).order_by(Conversation.last_message_at.desc()).all()  # Most recent first

        return {'conversations': [conv.to_dict() for conv in conversations]}, 200

    @jwt_required()  # Requires JWT token
    def post(self):
        """Create new conversation between two users
        Returns existing conversation if one already exists
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        data = request.get_json()
        errors = conversation_create_schema.validate(data)
        if errors:
            return {'errors': errors}, 400
        
        # Check if conversation already exists between these users
        existing_conv = Conversation.query.filter(
            ((Conversation.initiator_id == user.id) & (Conversation.participant_id == data['participant_id'])) |
            ((Conversation.initiator_id == data['participant_id']) & (Conversation.participant_id == user.id))
        ).first()
        
        if existing_conv:
            # Return existing conversation instead of creating duplicate
            return {'conversation': existing_conv.to_dict()}, 200
        
        # Create new conversation
        conversation = Conversation(
            initiator_id=user.id,  # Current user is sender
            participant_id=data['participant_id'],  # Other user is receiver
            property_id=data.get('property_id'),  # Optional property reference
            title=data.get('title')
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return {'conversation': conversation.to_dict()}, 201
class ConversationDetail(Resource):
    """Conversation detail endpoint - Get or delete specific conversation"""
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
    """Message list endpoint - Get messages or send new message"""
    @jwt_required()  # Requires JWT token
    def get(self, conversation_id):
        """Get all messages in a conversation
        Returns messages in chronological order (oldest first)
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        conversation = Conversation.query.get_or_404(conversation_id)

        # Verify user is part of this conversation
        if conversation.initiator_id != user.id and conversation.participant_id != user.id:
            return {'error': 'Access denied'}, 403

        # Get all messages in chronological order
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at.asc()).all()

        return {'messages': [msg.to_dict() for msg in messages]}, 200

    @jwt_required()  # Requires JWT token
    def post(self, conversation_id):
        """Send new message in conversation
        Creates message and updates conversation's last_message preview
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        conversation = Conversation.query.get_or_404(conversation_id)

        # Verify user is part of this conversation
        if conversation.initiator_id != user.id and conversation.participant_id != user.id:
            return {'error': 'Access denied'}, 403

        data = request.get_json()
        errors = message_create_schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        # Create new message
        message = Message(
            content=data['content'],
            conversation_id=conversation_id,
            sender_id=user.id  # Current user is sender
        )

        db.session.add(message)
        # Update conversation preview with latest message
        conversation.update_last_message(data['content'])
        db.session.commit()

        # For real-time updates, emit Socket.IO event (see app/sockets/__init__.py)
        return {'message': message.to_dict()}, 201