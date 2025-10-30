# ============================================================================
# CHAT MODEL - Real-time Messaging System
# ============================================================================
# Defines Conversation and Message models for landlord-tenant communication
#
# CONVERSATION FIELDS:
# - id: Primary key
# - initiator_id: User who started conversation (sender_id)
# - participant_id: Other user in conversation (receiver_id)
# - property_id: Related property (optional)
# - last_message: Preview of last message
# - last_message_at: Timestamp of last message
#
# MESSAGE FIELDS:
# - id: Primary key
# - content: Message text
# - sender_id: User who sent message
# - conversation_id: Parent conversation
# - timestamp: Message creation time (created_at)
#
# API ENDPOINTS:
# - GET /api/conversations - List all conversations
# - POST /api/conversations - Create new conversation
# - GET /api/conversations/<id>/messages - Get messages
# - POST /api/conversations/<id>/messages - Send message
#
# REAL-TIME UPDATES:
# - Socket.IO events for instant message delivery
# - Connect to socket: socketio.connect()
# - Listen for 'new_message' event
# - Emit 'send_message' event
# ============================================================================

from app.models.base import BaseModel
from app import db
from datetime import datetime

class Conversation(BaseModel):
    """Conversation model for chat threads between users"""
    __tablename__ = 'chat_conversations'

    title = db.Column(db.String(200))
    last_message = db.Column(db.Text)
    last_message_at = db.Column(db.DateTime)

    initiator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))

    initiator = db.relationship('User', back_populates='conversations_initiated', foreign_keys=[initiator_id])
    participant = db.relationship('User', back_populates='conversations_received', foreign_keys=[participant_id])
    property = db.relationship('Property', back_populates='conversations')
    messages = db.relationship('Message', back_populates='conversation', cascade='all, delete-orphan', order_by='Message.created_at')

    def to_dict(self):
        """Serialize conversation to dictionary for API responses
        Returns conversation with participant details and message preview
        """
        return {
            'id': self.id,
            'title': self.title,
            'last_message': self.last_message,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'initiator_id': self.initiator_id,  # sender_id
            'participant_id': self.participant_id,  # receiver_id
            'property_id': self.property_id,
            'initiator': self.initiator.to_dict() if self.initiator else None,
            'participant': self.participant.to_dict() if self.participant else None,
            'property': self.property.to_dict() if self.property else None,
            'message_count': len(self.messages),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def update_last_message(self, message_content):
        """Update conversation preview with latest message"""
        self.last_message = message_content
        self.last_message_at = datetime.utcnow()
        db.session.commit()

class Message(BaseModel):
    """Message model for individual chat messages"""
    __tablename__ = 'chat_messages'

    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)

    conversation_id = db.Column(db.Integer, db.ForeignKey('chat_conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    conversation = db.relationship('Conversation', back_populates='messages')
    sender = db.relationship('User', back_populates='messages')

    def to_dict(self):
        """Serialize message to dictionary for API responses
        Returns message with sender details and timestamp
        """
        return {
            'id': self.id,
            'content': self.content,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'sender': self.sender.to_dict() if self.sender else None,
            'timestamp': self.created_at.isoformat() if self.created_at else None,  # Frontend expects 'timestamp'
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def mark_as_read(self):
        """Mark message as read and update read timestamp"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
            db.session.commit()