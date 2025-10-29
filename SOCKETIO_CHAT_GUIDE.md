# Socket.IO Real-Time Chat Implementation Guide

## Backend Setup Complete ✓

The backend now supports real-time chat using Socket.IO with the following features:
- Real-time message delivery
- Typing indicators
- Read receipts
- Online user status
- JWT authentication

## Socket.IO Events

### Client → Server Events

#### 1. `authenticate`
Authenticate user with JWT token
```javascript
socket.emit('authenticate', {
  token: 'your-jwt-token'
});
```

#### 2. `join_conversation`
Join a conversation room
```javascript
socket.emit('join_conversation', {
  conversation_id: 1,
  user_id: 123
});
```

#### 3. `send_message`
Send a message
```javascript
socket.emit('send_message', {
  conversation_id: 1,
  user_id: 123,
  content: 'Hello!'
});
```

#### 4. `typing`
Send typing indicator
```javascript
socket.emit('typing', {
  conversation_id: 1,
  user_id: 123,
  is_typing: true
});
```

#### 5. `mark_read`
Mark messages as read
```javascript
socket.emit('mark_read', {
  conversation_id: 1,
  user_id: 123
});
```

#### 6. `leave_conversation`
Leave a conversation room
```javascript
socket.emit('leave_conversation', {
  conversation_id: 1,
  user_id: 123
});
```

#### 7. `get_online_users`
Get list of online users
```javascript
socket.emit('get_online_users');
```

### Server → Client Events

#### 1. `connected`
Connection established
```javascript
socket.on('connected', (data) => {
  console.log(data.message);
});
```

#### 2. `authenticated`
Authentication successful
```javascript
socket.on('authenticated', (data) => {
  console.log('User ID:', data.user_id);
  console.log('User:', data.user);
});
```

#### 3. `joined_conversation`
Successfully joined conversation
```javascript
socket.on('joined_conversation', (data) => {
  console.log('Joined conversation:', data.conversation_id);
});
```

#### 4. `new_message`
New message received
```javascript
socket.on('new_message', (message) => {
  console.log('New message:', message);
  // Add message to UI
});
```

#### 5. `user_typing`
User is typing
```javascript
socket.on('user_typing', (data) => {
  if (data.is_typing) {
    showTypingIndicator(data.user_id);
  } else {
    hideTypingIndicator(data.user_id);
  }
});
```

#### 6. `messages_read`
Messages marked as read
```javascript
socket.on('messages_read', (data) => {
  console.log('Messages read:', data.message_ids);
  // Update UI to show read status
});
```

#### 7. `message_notification`
New message notification (when not in conversation)
```javascript
socket.on('message_notification', (data) => {
  showNotification(data.message);
});
```

#### 8. `online_users`
List of online users
```javascript
socket.on('online_users', (data) => {
  console.log('Online users:', data.user_ids);
});
```

#### 9. `error`
Error occurred
```javascript
socket.on('error', (data) => {
  console.error('Socket error:', data.message);
});
```

## Frontend Implementation (React)

### Install Socket.IO Client
```bash
npm install socket.io-client
```

### Create Socket Service

```javascript
// services/socketService.js
import io from 'socket.io-client';

const SOCKET_URL = 'https://landlord-app-backend-1eph.onrender.com';

class SocketService {
  constructor() {
    this.socket = null;
    this.connected = false;
  }

  connect(token) {
    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5
    });

    this.socket.on('connect', () => {
      console.log('Socket connected');
      this.connected = true;
      this.authenticate(token);
    });

    this.socket.on('disconnect', () => {
      console.log('Socket disconnected');
      this.connected = false;
    });

    this.socket.on('error', (data) => {
      console.error('Socket error:', data.message);
    });
  }

  authenticate(token) {
    this.socket.emit('authenticate', { token });
  }

  joinConversation(conversationId, userId) {
    this.socket.emit('join_conversation', {
      conversation_id: conversationId,
      user_id: userId
    });
  }

  leaveConversation(conversationId, userId) {
    this.socket.emit('leave_conversation', {
      conversation_id: conversationId,
      user_id: userId
    });
  }

  sendMessage(conversationId, userId, content) {
    this.socket.emit('send_message', {
      conversation_id: conversationId,
      user_id: userId,
      content
    });
  }

  sendTyping(conversationId, userId, isTyping) {
    this.socket.emit('typing', {
      conversation_id: conversationId,
      user_id: userId,
      is_typing: isTyping
    });
  }

  markRead(conversationId, userId) {
    this.socket.emit('mark_read', {
      conversation_id: conversationId,
      user_id: userId
    });
  }

  onNewMessage(callback) {
    this.socket.on('new_message', callback);
  }

  onUserTyping(callback) {
    this.socket.on('user_typing', callback);
  }

  onMessagesRead(callback) {
    this.socket.on('messages_read', callback);
  }

  onMessageNotification(callback) {
    this.socket.on('message_notification', callback);
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }
}

export default new SocketService();
```

### Chat Component with Socket.IO

```javascript
// components/ChatWindow.jsx
import React, { useState, useEffect, useRef } from 'react';
import socketService from '../services/socketService';
import axios from 'axios';

const ChatWindow = ({ conversationId, currentUserId, token }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [otherUserTyping, setOtherUserTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  useEffect(() => {
    // Connect socket
    socketService.connect(token);

    // Load initial messages
    loadMessages();

    // Join conversation
    socketService.joinConversation(conversationId, currentUserId);

    // Listen for new messages
    socketService.onNewMessage((message) => {
      if (message.conversation_id === conversationId) {
        setMessages(prev => [...prev, message]);
        
        // Mark as read if not sent by current user
        if (message.sender_id !== currentUserId) {
          socketService.markRead(conversationId, currentUserId);
        }
      }
    });

    // Listen for typing indicator
    socketService.onUserTyping((data) => {
      if (data.conversation_id === conversationId) {
        setOtherUserTyping(data.is_typing);
      }
    });

    // Listen for read receipts
    socketService.onMessagesRead((data) => {
      if (data.conversation_id === conversationId) {
        setMessages(prev => prev.map(msg => 
          data.message_ids.includes(msg.id) 
            ? { ...msg, is_read: true } 
            : msg
        ));
      }
    });

    return () => {
      socketService.leaveConversation(conversationId, currentUserId);
    };
  }, [conversationId, currentUserId, token]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadMessages = async () => {
    try {
      const response = await axios.get(
        `https://landlord-app-backend-1eph.onrender.com/api/conversations/${conversationId}/messages`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessages(response.data.messages);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    socketService.sendMessage(conversationId, currentUserId, newMessage);
    setNewMessage('');
    
    // Stop typing indicator
    if (isTyping) {
      socketService.sendTyping(conversationId, currentUserId, false);
      setIsTyping(false);
    }
  };

  const handleTyping = (e) => {
    setNewMessage(e.target.value);

    // Send typing indicator
    if (!isTyping) {
      socketService.sendTyping(conversationId, currentUserId, true);
      setIsTyping(true);
    }

    // Clear previous timeout
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }

    // Stop typing after 2 seconds of inactivity
    typingTimeoutRef.current = setTimeout(() => {
      socketService.sendTyping(conversationId, currentUserId, false);
      setIsTyping(false);
    }, 2000);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map(msg => (
          <div
            key={msg.id}
            className={`message ${msg.sender_id === currentUserId ? 'sent' : 'received'}`}
          >
            <div className="message-content">{msg.content}</div>
            <div className="message-meta">
              <span className="message-time">
                {new Date(msg.created_at).toLocaleTimeString()}
              </span>
              {msg.sender_id === currentUserId && msg.is_read && (
                <span className="read-indicator">✓✓</span>
              )}
            </div>
          </div>
        ))}
        {otherUserTyping && (
          <div className="typing-indicator">
            <span>Typing</span>
            <span className="dots">...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="message-input">
        <input
          type="text"
          value={newMessage}
          onChange={handleTyping}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatWindow;
```

### CSS Styling

```css
.chat-window {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f5f5;
}

.message {
  margin-bottom: 15px;
  max-width: 70%;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.sent {
  margin-left: auto;
  text-align: right;
}

.message.received {
  margin-right: auto;
}

.message-content {
  padding: 10px 15px;
  border-radius: 18px;
  display: inline-block;
  word-wrap: break-word;
}

.message.sent .message-content {
  background: #007bff;
  color: white;
}

.message.received .message-content {
  background: white;
  color: #333;
  border: 1px solid #e0e0e0;
}

.message-meta {
  font-size: 0.75rem;
  color: #666;
  margin-top: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.read-indicator {
  color: #007bff;
  font-weight: bold;
}

.typing-indicator {
  padding: 10px;
  color: #666;
  font-style: italic;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.message-input {
  display: flex;
  padding: 15px;
  border-top: 1px solid #ddd;
  background: white;
}

.message-input input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin-right: 10px;
  outline: none;
}

.message-input input:focus {
  border-color: #007bff;
}

.message-input button {
  padding: 10px 25px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.message-input button:hover {
  background: #0056b3;
}
```

## Testing the Socket.IO Chat

### 1. Test Connection
```javascript
// In browser console
const socket = io('https://landlord-app-backend-1eph.onrender.com');
socket.on('connected', (data) => console.log(data));
```

### 2. Test Authentication
```javascript
socket.emit('authenticate', { token: 'your-jwt-token' });
socket.on('authenticated', (data) => console.log(data));
```

### 3. Test Messaging
```javascript
socket.emit('join_conversation', { conversation_id: 1, user_id: 123 });
socket.emit('send_message', { 
  conversation_id: 1, 
  user_id: 123, 
  content: 'Test message' 
});
socket.on('new_message', (msg) => console.log(msg));
```

## Deployment Notes

### Render.com Configuration
The backend is already configured for Socket.IO. Ensure:
- `eventlet` is in requirements.txt ✓
- `Flask-SocketIO` is in requirements.txt ✓
- CORS is configured for your frontend domain ✓

### Environment Variables
No additional environment variables needed for Socket.IO.

## Features Implemented

✅ Real-time message delivery
✅ Typing indicators
✅ Read receipts
✅ Online user status
✅ JWT authentication
✅ Room-based conversations
✅ Message notifications
✅ Automatic reconnection
✅ Error handling

## Next Steps

1. Install socket.io-client in frontend: `npm install socket.io-client`
2. Copy the SocketService code to your frontend
3. Integrate ChatWindow component
4. Add chat UI to landlord and tenant dashboards
5. Test with multiple users
6. Deploy and verify

The Socket.IO chat system is now fully implemented on the backend!
