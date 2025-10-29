# Chat System Integration Guide

## Backend API Endpoints

### 1. List Conversations
```
GET /api/conversations
Headers: Authorization: Bearer <token>
Response: { conversations: [...] }
```

### 2. Create Conversation
```
POST /api/conversations
Headers: Authorization: Bearer <token>
Body: {
  "participant_id": 2,
  "property_id": 1,  // optional
  "title": "Property Inquiry"  // optional
}
Response: { conversation: {...} }
```

### 3. Get Conversation Messages
```
GET /api/conversations/{id}/messages
Headers: Authorization: Bearer <token>
Response: { messages: [...] }
```

### 4. Send Message
```
POST /api/conversations/{id}/messages
Headers: Authorization: Bearer <token>
Body: {
  "content": "Hello, I'm interested in this property"
}
Response: { message: {...} }
```

## Frontend Implementation Example (React)

### ChatList Component
```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ChatList = ({ token }) => {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const response = await axios.get(
        'https://landlord-app-backend-1eph.onrender.com/api/conversations',
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setConversations(response.data.conversations);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading conversations...</div>;

  return (
    <div className="chat-list">
      <h2>Messages</h2>
      {conversations.length === 0 ? (
        <p>No conversations yet</p>
      ) : (
        conversations.map(conv => (
          <div key={conv.id} className="conversation-item">
            <h3>{conv.title || 'Conversation'}</h3>
            <p>{conv.last_message}</p>
            <small>{new Date(conv.last_message_at).toLocaleString()}</small>
          </div>
        ))
      )}
    </div>
  );
};

export default ChatList;
```

### ChatWindow Component
```jsx
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const ChatWindow = ({ conversationId, token, currentUserId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchMessages();
    // Poll for new messages every 3 seconds
    const interval = setInterval(fetchMessages, 3000);
    return () => clearInterval(interval);
  }, [conversationId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchMessages = async () => {
    try {
      const response = await axios.get(
        `https://landlord-app-backend-1eph.onrender.com/api/conversations/${conversationId}/messages`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setMessages(response.data.messages);
    } catch (error) {
      console.error('Error fetching messages:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      const response = await axios.post(
        `https://landlord-app-backend-1eph.onrender.com/api/conversations/${conversationId}/messages`,
        { content: newMessage },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setMessages([...messages, response.data.message]);
      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  if (loading) return <div>Loading messages...</div>;

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map(msg => (
          <div
            key={msg.id}
            className={`message ${msg.sender_id === currentUserId ? 'sent' : 'received'}`}
          >
            <div className="message-content">{msg.content}</div>
            <div className="message-time">
              {new Date(msg.created_at).toLocaleTimeString()}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="message-input">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatWindow;
```

### Start New Conversation
```jsx
const startConversation = async (participantId, propertyId = null) => {
  try {
    const response = await axios.post(
      'https://landlord-app-backend-1eph.onrender.com/api/conversations',
      {
        participant_id: participantId,
        property_id: propertyId,
        title: propertyId ? 'Property Inquiry' : 'New Conversation'
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );
    return response.data.conversation;
  } catch (error) {
    console.error('Error creating conversation:', error);
  }
};
```

## CSS Styling Example

```css
.chat-list {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  max-width: 400px;
}

.conversation-item {
  padding: 15px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s;
}

.conversation-item:hover {
  background: #f5f5f5;
}

.chat-window {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f9f9f9;
}

.message {
  margin-bottom: 15px;
  max-width: 70%;
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
}

.message.sent .message-content {
  background: #007bff;
  color: white;
}

.message.received .message-content {
  background: #e9ecef;
  color: #333;
}

.message-time {
  font-size: 0.75rem;
  color: #666;
  margin-top: 5px;
}

.message-input {
  display: flex;
  padding: 15px;
  border-top: 1px solid #ddd;
  background: white;
}

.message-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin-right: 10px;
}

.message-input button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.message-input button:hover {
  background: #0056b3;
}
```

## Integration in Dashboard

### Landlord Dashboard
```jsx
import ChatList from './components/ChatList';
import ChatWindow from './components/ChatWindow';

const LandlordDashboard = () => {
  const [selectedConversation, setSelectedConversation] = useState(null);
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('userId');

  return (
    <div className="dashboard">
      <div className="sidebar">
        <ChatList 
          token={token}
          onSelectConversation={setSelectedConversation}
        />
      </div>
      <div className="main-content">
        {selectedConversation ? (
          <ChatWindow
            conversationId={selectedConversation.id}
            token={token}
            currentUserId={userId}
          />
        ) : (
          <div>Select a conversation to start chatting</div>
        )}
      </div>
    </div>
  );
};
```

### Tenant Dashboard
Same implementation as Landlord Dashboard - the backend automatically handles permissions.

## Real-Time Updates

For real-time messaging, you have two options:

### Option 1: Polling (Simple)
```javascript
// Already implemented in ChatWindow component
// Fetches messages every 3 seconds
useEffect(() => {
  const interval = setInterval(fetchMessages, 3000);
  return () => clearInterval(interval);
}, [conversationId]);
```

### Option 2: WebSocket (Advanced)
```javascript
// Install socket.io-client
// npm install socket.io-client

import io from 'socket.io-client';

const socket = io('https://landlord-app-backend-1eph.onrender.com');

socket.on('new_message', (message) => {
  if (message.conversation_id === conversationId) {
    setMessages(prev => [...prev, message]);
  }
});

socket.emit('join_conversation', conversationId);
```

## Testing the Chat System

1. **Create two users** (one landlord, one tenant)
2. **Login as tenant** and view a property
3. **Click "Contact Landlord"** button
4. **Send a message**
5. **Login as landlord** and check messages
6. **Reply to the message**
7. **Switch back to tenant** and see the reply

## Common Issues & Solutions

### Issue: Messages not updating
**Solution**: Check if polling interval is working or increase frequency

### Issue: Can't send messages
**Solution**: Verify token is valid and conversation_id is correct

### Issue: Conversation not created
**Solution**: Ensure participant_id exists and is different from current user

### Issue: CORS errors
**Solution**: Backend already configured for CORS, check frontend URL

## API Response Examples

### Conversation Object
```json
{
  "id": 1,
  "title": "Property Inquiry",
  "last_message": "Hello, I'm interested",
  "last_message_at": "2024-01-15T10:30:00",
  "initiator_id": 2,
  "participant_id": 1,
  "property_id": 5,
  "initiator": {
    "id": 2,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  },
  "participant": {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com"
  }
}
```

### Message Object
```json
{
  "id": 1,
  "content": "Hello, I'm interested in this property",
  "is_read": false,
  "conversation_id": 1,
  "sender_id": 2,
  "sender": {
    "id": 2,
    "first_name": "John",
    "last_name": "Doe"
  },
  "created_at": "2024-01-15T10:30:00"
}
```

## Next Steps

1. ✅ Backend chat API is ready
2. ✅ Implement frontend components using examples above
3. ✅ Add "Contact Landlord" button on property details page
4. ✅ Add chat icon/badge in navigation with unread count
5. ✅ Test with multiple users
6. ✅ Deploy and verify in production

The chat system is fully functional on the backend. Just integrate these components into your frontend!
