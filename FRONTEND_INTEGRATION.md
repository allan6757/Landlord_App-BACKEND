## Frontend Integration Guide - PropManager API

## 🌐 Deployment URLs

**Backend API:** https://landlord-app-backend-1eph.onrender.com  
**Frontend App:** https://landlord-app-frontend.vercel.app

---

## 🎯 Quick Reference for React Frontend

### Base URL Configuration

**For Development (localhost):**
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

**For Production (deployed):**
```javascript
const API_BASE_URL = 'https://landlord-app-backend-1eph.onrender.com/api';
```

**Recommended: Use Environment Variables**

Create a `.env` file in your React project root:
```bash
# .env.development
REACT_APP_API_BASE_URL=http://localhost:5000/api

# .env.production
REACT_APP_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
```

Then use in your code:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';
```

**For Vite:**
```bash
# .env
VITE_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
```
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
```

---

## 🔐 Authentication Flow

### 1. Register User
```javascript
// POST /api/auth/register
const register = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: userData.email,
      password: userData.password,
      first_name: userData.firstName,
      last_name: userData.lastName,
      role: userData.role  // 'landlord' or 'tenant'
    })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Store token in localStorage
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data.user;
  } else {
    throw new Error(data.error || 'Registration failed');
  }
};
```

### 2. Login User
```javascript
// POST /api/auth/login
const login = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data.user;
  } else {
    throw new Error(data.error || 'Login failed');
  }
};
```

### 3. Get Current User Profile
```javascript
// GET /api/auth/profile
const getProfile = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/auth/profile`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = await response.json();
  return data.user;
};
```

### 4. Check User Role
```javascript
const getUserRole = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  return user?.profile?.role;  // 'landlord' or 'tenant'
};

const isLandlord = () => getUserRole() === 'landlord';
const isTenant = () => getUserRole() === 'tenant';
```

---

## 🏠 Property Management

### 1. Get Properties
```javascript
// GET /api/properties
// Returns properties based on user role:
// - Landlord: properties they own
// - Tenant: properties assigned to them
const getProperties = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/properties`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = await response.json();
  return data.properties;  // Array of property objects
};
```

### 2. Create Property (Landlord Only)
```javascript
// POST /api/properties
const createProperty = async (propertyData) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/properties`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      title: propertyData.title,
      address: propertyData.address,
      city: propertyData.city,
      state: propertyData.state,
      zip_code: propertyData.zipCode,
      property_type: propertyData.propertyType,  // 'apartment', 'house', etc.
      monthly_rent: propertyData.monthlyRent,
      bedrooms: propertyData.bedrooms,
      bathrooms: propertyData.bathrooms,
      status: 'vacant'  // or 'occupied'
    })
  });
  
  const data = await response.json();
  return data.property;
};
```

### 3. Update Property (Landlord Only)
```javascript
// PUT /api/properties/<id>
const updateProperty = async (propertyId, updates) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/properties/${propertyId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(updates)
  });
  
  const data = await response.json();
  return data.property;
};
```

### 4. Property Status Values
```javascript
// Property status can be:
const PROPERTY_STATUS = {
  VACANT: 'vacant',      // Available for rent
  OCCUPIED: 'occupied',  // Currently rented
  MAINTENANCE: 'maintenance',
  UNAVAILABLE: 'unavailable'
};
```

---

## 💳 Payment Management

### 1. Get Payments
```javascript
// GET /api/payments
// Returns payments based on user role:
// - Landlord: payments for their properties
// - Tenant: their own payments
const getPayments = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/payments`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = await response.json();
  return data.payments;  // Array of payment objects
};
```

### 2. Create Payment with M-Pesa
```javascript
// POST /api/payments
// Initiates M-Pesa STK Push to user's phone
const createPayment = async (propertyId, amount, phoneNumber) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/payments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      property_id: propertyId,
      amount: amount,
      phone_number: phoneNumber,  // Format: 254712345678
      payment_method: 'mpesa'
    })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Payment created, STK Push sent to phone
    // User will receive prompt on their phone to enter M-Pesa PIN
    return data.payment;
  } else {
    throw new Error(data.error || 'Payment failed');
  }
};
```

### 3. Payment Status Values
```javascript
// Payment status can be:
const PAYMENT_STATUS = {
  PENDING: 'pending',      // Awaiting payment
  COMPLETED: 'completed',  // Payment successful
  FAILED: 'failed',        // Payment failed
  CANCELLED: 'cancelled'   // Payment cancelled
};
```

### 4. Phone Number Format for M-Pesa
```javascript
// M-Pesa requires Kenyan phone format: 254XXXXXXXXX
const formatPhoneNumber = (phone) => {
  // Remove spaces, dashes, and plus signs
  phone = phone.replace(/[\s\-\+]/g, '');
  
  // If starts with 0, replace with 254
  if (phone.startsWith('0')) {
    phone = '254' + phone.substring(1);
  }
  
  // If starts with 7 or 1, add 254
  if (phone.startsWith('7') || phone.startsWith('1')) {
    phone = '254' + phone;
  }
  
  return phone;
};

// Example usage:
// formatPhoneNumber('0712345678') => '254712345678'
// formatPhoneNumber('+254712345678') => '254712345678'
```

---

## 💬 Chat/Messaging

### 1. Get Conversations
```javascript
// GET /api/conversations
const getConversations = async () => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  const data = await response.json();
  return data.conversations;  // Array of conversation objects
};
```

### 2. Create Conversation
```javascript
// POST /api/conversations
const createConversation = async (participantId, propertyId = null) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      participant_id: participantId,  // User to chat with
      property_id: propertyId         // Optional: related property
    })
  });
  
  const data = await response.json();
  return data.conversation;
};
```

### 3. Get Messages
```javascript
// GET /api/conversations/<id>/messages
const getMessages = async (conversationId) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}/messages`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  const data = await response.json();
  return data.messages;  // Array of message objects
};
```

### 4. Send Message
```javascript
// POST /api/conversations/<id>/messages
const sendMessage = async (conversationId, content) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}/messages`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ content })
    }
  );
  
  const data = await response.json();
  return data.message;
};
```

---

## 🔄 Complete React Context Example

```javascript
// AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load user from localStorage on mount
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
      setToken(data.token);
      setUser(data.user);
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      return data.user;
    } else {
      throw new Error(data.error || 'Login failed');
    }
  };

  const register = async (userData) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });

    const data = await response.json();

    if (response.ok) {
      setToken(data.token);
      setUser(data.user);
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
      return data.user;
    } else {
      throw new Error(data.error || 'Registration failed');
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const isLandlord = () => user?.profile?.role === 'landlord';
  const isTenant = () => user?.profile?.role === 'tenant';

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      login,
      register,
      logout,
      isLandlord,
      isTenant
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

---

## 🛠️ API Helper Functions

```javascript
// api.js - Centralized API helper
const API_BASE_URL = 'http://localhost:5000/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
};

const handleResponse = async (response) => {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Request failed');
  }
  return data;
};

export const api = {
  // Auth
  login: (email, password) =>
    fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    }).then(handleResponse),

  register: (userData) =>
    fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    }).then(handleResponse),

  getProfile: () =>
    fetch(`${API_BASE_URL}/auth/profile`, {
      headers: getAuthHeaders()
    }).then(handleResponse),

  // Properties
  getProperties: () =>
    fetch(`${API_BASE_URL}/properties`, {
      headers: getAuthHeaders()
    }).then(handleResponse),

  createProperty: (propertyData) =>
    fetch(`${API_BASE_URL}/properties`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(propertyData)
    }).then(handleResponse),

  updateProperty: (id, updates) =>
    fetch(`${API_BASE_URL}/properties/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updates)
    }).then(handleResponse),

  // Payments
  getPayments: () =>
    fetch(`${API_BASE_URL}/payments`, {
      headers: getAuthHeaders()
    }).then(handleResponse),

  createPayment: (paymentData) =>
    fetch(`${API_BASE_URL}/payments`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(paymentData)
    }).then(handleResponse),

  // Chat
  getConversations: () =>
    fetch(`${API_BASE_URL}/conversations`, {
      headers: getAuthHeaders()
    }).then(handleResponse),

  createConversation: (participantId, propertyId) =>
    fetch(`${API_BASE_URL}/conversations`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ participant_id: participantId, property_id: propertyId })
    }).then(handleResponse),

  getMessages: (conversationId) =>
    fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      headers: getAuthHeaders()
    }).then(handleResponse),

  sendMessage: (conversationId, content) =>
    fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ content })
    }).then(handleResponse)
};
```

---

## 📊 Data Structure Reference

### User Object
```javascript
{
  id: 1,
  email: "user@example.com",
  first_name: "John",
  profile: {
    id: 1,
    role: "tenant"  // or "landlord"
  }
}
```

### Property Object
```javascript
{
  id: 1,
  title: "Modern Apartment",
  monthly_rent: 1500.00,
  status: "occupied",  // or "vacant"
  landlord_id: 2,
  tenant_id: 3,
  address: "123 Main St",
  city: "Nairobi",
  bedrooms: 2,
  bathrooms: 1
}
```

### Payment Object
```javascript
{
  id: 1,
  amount: 1500.00,
  status: "completed",  // pending/completed/failed
  due_date: "2024-01-15T00:00:00",
  property_id: 1,
  tenant_id: 3,
  property: { /* property object */ },
  tenant: { /* user object */ }
}
```

### Message Object
```javascript
{
  id: 1,
  sender_id: 2,
  content: "Hello, is the property available?",
  timestamp: "2024-01-15T10:30:00",
  is_read: false,
  conversation_id: 1
}
```

---

## ⚠️ Error Handling

```javascript
const handleApiError = (error) => {
  if (error.message.includes('401')) {
    // Unauthorized - redirect to login
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  } else if (error.message.includes('403')) {
    // Forbidden - show access denied message
    alert('Access denied');
  } else {
    // Other errors
    console.error('API Error:', error);
    alert(error.message || 'An error occurred');
  }
};

// Usage:
try {
  const properties = await api.getProperties();
} catch (error) {
  handleApiError(error);
}
```

---

## 🚀 Quick Start Checklist

- [ ] Set API_BASE_URL to backend URL
- [ ] Implement authentication (login/register)
- [ ] Store JWT token in localStorage
- [ ] Include token in all API requests
- [ ] Check user role (user.profile.role)
- [ ] Implement role-based UI (landlord vs tenant views)
- [ ] Handle API errors and unauthorized access
- [ ] Format phone numbers for M-Pesa (254XXXXXXXXX)
- [ ] Test all CRUD operations
- [ ] Implement real-time chat with Socket.IO (optional)
