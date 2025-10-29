"""
Socket.IO Event Handlers for Real-Time Chat
"""
from flask import request
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token
from app import socketio, db
from app.models import User, Conversation, Message
from datetime import datetime

# Store active users and their socket IDs
active_users = {}

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('connected', {'message': 'Connected to chat server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    for user_id, sid in list(active_users.items()):
        if sid == request.sid:
            del active_users[user_id]
            print(f'User {user_id} disconnected')
            break
    print(f'Client disconnected: {request.sid}')

@socketio.on('authenticate')
def handle_authenticate(data):
    """Authenticate user with JWT token"""
    try:
        token = data.get('token')
        if not token:
            emit('error', {'message': 'No token provided'})
            return
        
        decoded = decode_token(token)
        user_id = decoded['sub']
        active_users[user_id] = request.sid
        
        user = User.query.get(user_id)
        if user:
            emit('authenticated', {'user_id': user_id, 'user': user.to_dict()})
            print(f'User {user_id} authenticated')
        else:
            emit('error', {'message': 'User not found'})
    except Exception as e:
        print(f'Authentication error: {str(e)}')
        emit('error', {'message': 'Authentication failed'})

@socketio.on('join_conversation')
def handle_join_conversation(data):
    """Join a conversation room"""
    try:
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')
        
        if not conversation_id or not user_id:
            emit('error', {'message': 'Missing conversation_id or user_id'})
            return
        
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            emit('error', {'message': 'Conversation not found'})
            return
        
        if conversation.initiator_id != user_id and conversation.participant_id != user_id:
            emit('error', {'message': 'Access denied'})
            return
        
        room = f'conversation_{conversation_id}'
        join_room(room)
        
        emit('joined_conversation', {'conversation_id': conversation_id, 'room': room})
        
        other_user_id = conversation.participant_id if conversation.initiator_id == user_id else conversation.initiator_id
        if other_user_id in active_users:
            emit('user_joined', {'user_id': user_id, 'conversation_id': conversation_id}, room=active_users[other_user_id])
        
        print(f'User {user_id} joined conversation {conversation_id}')
    except Exception as e:
        print(f'Join conversation error: {str(e)}')
        emit('error', {'message': 'Failed to join conversation'})

@socketio.on('leave_conversation')
def handle_leave_conversation(data):
    """Leave a conversation room"""
    try:
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')
        
        room = f'conversation_{conversation_id}'
        leave_room(room)
        
        emit('left_conversation', {'conversation_id': conversation_id})
        
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            other_user_id = conversation.participant_id if conversation.initiator_id == user_id else conversation.initiator_id
            if other_user_id in active_users:
                emit('user_left', {'user_id': user_id, 'conversation_id': conversation_id}, room=active_users[other_user_id])
        
        print(f'User {user_id} left conversation {conversation_id}')
    except Exception as e:
        print(f'Leave conversation error: {str(e)}')

@socketio.on('send_message')
def handle_send_message(data):
    """Handle sending a message"""
    try:
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')
        content = data.get('content', '').strip()
        
        if not conversation_id or not user_id or not content:
            emit('error', {'message': 'Missing required fields'})
            return
        
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            emit('error', {'message': 'Conversation not found'})
            return
        
        if conversation.initiator_id != user_id and conversation.participant_id != user_id:
            emit('error', {'message': 'Access denied'})
            return
        
        message = Message(content=content, conversation_id=conversation_id, sender_id=user_id)
        db.session.add(message)
        
        conversation.last_message = content
        conversation.last_message_at = datetime.utcnow()
        db.session.commit()
        
        sender = User.query.get(user_id)
        message_data = {
            'id': message.id,
            'content': message.content,
            'conversation_id': conversation_id,
            'sender_id': user_id,
            'sender': {'id': sender.id, 'first_name': sender.first_name, 'last_name': sender.last_name, 'profile_image': sender.profile_image},
            'is_read': False,
            'created_at': message.created_at.isoformat()
        }
        
        room = f'conversation_{conversation_id}'
        emit('new_message', message_data, room=room, include_self=True)
        
        other_user_id = conversation.participant_id if conversation.initiator_id == user_id else conversation.initiator_id
        if other_user_id in active_users:
            emit('message_notification', {'conversation_id': conversation_id, 'message': message_data}, room=active_users[other_user_id])
        
        print(f'Message sent in conversation {conversation_id} by user {user_id}')
    except Exception as e:
        print(f'Send message error: {str(e)}')
        db.session.rollback()
        emit('error', {'message': 'Failed to send message'})

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    try:
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')
        is_typing = data.get('is_typing', False)
        
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            other_user_id = conversation.participant_id if conversation.initiator_id == user_id else conversation.initiator_id
            if other_user_id in active_users:
                emit('user_typing', {'conversation_id': conversation_id, 'user_id': user_id, 'is_typing': is_typing}, room=active_users[other_user_id])
    except Exception as e:
        print(f'Typing indicator error: {str(e)}')

@socketio.on('mark_read')
def handle_mark_read(data):
    """Mark messages as read"""
    try:
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')
        
        unread_messages = Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.is_read == False
        ).all()
        
        for message in unread_messages:
            message.is_read = True
            message.read_at = datetime.utcnow()
        
        db.session.commit()
        
        if unread_messages:
            conversation = Conversation.query.get(conversation_id)
            other_user_id = conversation.participant_id if conversation.initiator_id == user_id else conversation.initiator_id
            
            if other_user_id in active_users:
                emit('messages_read', {'conversation_id': conversation_id, 'read_by': user_id, 'message_ids': [msg.id for msg in unread_messages]}, room=active_users[other_user_id])
        
        emit('marked_read', {'conversation_id': conversation_id, 'count': len(unread_messages)})
    except Exception as e:
        print(f'Mark read error: {str(e)}')
        db.session.rollback()

@socketio.on('get_online_users')
def handle_get_online_users():
    """Get list of online users"""
    emit('online_users', {'user_ids': list(active_users.keys())})
