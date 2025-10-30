# 🚨 URGENT FRONTEND FIX GUIDE

## Critical Issues to Fix

1. ❌ Can't sign in
2. ❌ Can't add properties
3. ❌ Can't view chats
4. ❌ Landlord and tenant views show same data

---

## 🔧 STEP 1: Fix API Base URL

### In your frontend `.env` file:
```bash
VITE_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
# OR for React
REACT_APP_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
```

### In your API service file (api.js or config.js):
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
                     process.env.REACT_APP_API_BASE_URL || 
                     'https://landlord-app-backend-1eph.onrender.com/api';

export default API_BASE_URL;
```

---

## 🔧 STEP 2: Fix Authentication (Sign In Issue)

### The Problem:
Your backend returns this structure:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "profile": {
      "id": 1,
      "role": "landlord"
    }
  }
}
```

### Fix Your Login Function:
```javascript
// auth.js or AuthContext.js
const login = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }
    
    // CRITICAL: Store token and user correctly
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data.user;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};
```

### Fix Your Register Function:
```javascript
const register = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        first_name: userData.firstName,
        last_name: userData.lastName,
        role: userData.role  // MUST be 'landlord' or 'tenant'
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }
    
    // Store token and user
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data.user;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};
```

---

## 🔧 STEP 3: Fix Role-Based Views (CRITICAL!)

### The Problem:
Both landlord and tenant see the same data because you're not checking the role correctly.

### Fix: Get User Role Correctly
```javascript
// utils/auth.js or helpers.js
export const getUser = () => {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  return JSON.parse(userStr);
};

export const getUserRole = () => {
  const user = getUser();
  // CRITICAL: Access role from profile object
  return user?.profile?.role;
};

export const isLandlord = () => {
  return getUserRole() === 'landlord';
};

export const isTenant = () => {
  return getUserRole() === 'tenant';
};

export const getToken = () => {
  return localStorage.getItem('token');
};
```

### Fix: Conditional Rendering Based on Role
```javascript
// In your Dashboard or Main Component
import { isLandlord, isTenant } from './utils/auth';

function Dashboard() {
  const userRole = getUserRole();
  
  return (
    <div>
      {isLandlord() && <LandlordDashboard />}
      {isTenant() && <TenantDashboard />}
    </div>
  );
}
```

### Fix: Show/Hide Features Based on Role
```javascript
// In your Navigation or Sidebar
function Navigation() {
  return (
    <nav>
      {/* Everyone can see these */}
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/properties">Properties</Link>
      
      {/* Only landlords can see these */}
      {isLandlord() && (
        <>
          <Link to="/properties/new">Add Property</Link>
          <Link to="/tenants">My Tenants</Link>
        </>
      )}
      
      {/* Only tenants can see these */}
      {isTenant() && (
        <>
          <Link to="/payments">My Payments</Link>
          <Link to="/maintenance">Maintenance Requests</Link>
        </>
      )}
      
      {/* Everyone can see chat */}
      <Link to="/chat">Messages</Link>
    </nav>
  );
}
```

---

## 🔧 STEP 4: Fix Property Management

### The Problem:
Backend filters properties by role automatically, but you need to send the token.

### Fix: Get Properties with Authentication
```javascript
const getProperties = async () => {
  try {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('Not authenticated');
    }
    
    const response = await fetch(`${API_BASE_URL}/properties`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch properties');
    }
    
    // Backend returns { properties: [...] }
    return data.properties;
  } catch (error) {
    console.error('Get properties error:', error);
    throw error;
  }
};
```

### Fix: Create Property (Landlord Only)
```javascript
const createProperty = async (propertyData) => {
  try {
    const token = localStorage.getItem('token');
    
    // Check if user is landlord
    if (!isLandlord()) {
      throw new Error('Only landlords can create properties');
    }
    
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
        property_type: propertyData.propertyType,
        monthly_rent: propertyData.monthlyRent,
        bedrooms: propertyData.bedrooms,
        bathrooms: propertyData.bathrooms,
        description: propertyData.description,
        status: 'vacant'
      })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to create property');
    }
    
    return data.property;
  } catch (error) {
    console.error('Create property error:', error);
    throw error;
  }
};
```

---

## 🔧 STEP 5: Fix Chat/Messaging

### Fix: Get Conversations
```javascript
const getConversations = async () => {
  try {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/conversations`, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch conversations');
    }
    
    return data.conversations || [];
  } catch (error) {
    console.error('Get conversations error:', error);
    throw error;
  }
};
```

### Fix: Send Message
```javascript
const sendMessage = async (conversationId, content) => {
  try {
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
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to send message');
    }
    
    return data.message;
  } catch (error) {
    console.error('Send message error:', error);
    throw error;
  }
};
```

---

## 🔧 STEP 6: Protected Routes

### Create a ProtectedRoute Component:
```javascript
// components/ProtectedRoute.jsx
import { Navigate } from 'react-router-dom';
import { getToken, getUserRole } from '../utils/auth';

function ProtectedRoute({ children, allowedRoles }) {
  const token = getToken();
  const userRole = getUserRole();
  
  if (!token) {
    // Not logged in, redirect to login
    return <Navigate to="/login" replace />;
  }
  
  if (allowedRoles && !allowedRoles.includes(userRole)) {
    // Wrong role, redirect to dashboard
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
}

export default ProtectedRoute;
```

### Use Protected Routes:
```javascript
// App.jsx or Routes.jsx
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      {/* Protected routes for all authenticated users */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      
      {/* Landlord-only routes */}
      <Route path="/properties/new" element={
        <ProtectedRoute allowedRoles={['landlord']}>
          <CreateProperty />
        </ProtectedRoute>
      } />
      
      {/* Tenant-only routes */}
      <Route path="/payments" element={
        <ProtectedRoute allowedRoles={['tenant']}>
          <Payments />
        </ProtectedRoute>
      } />
    </Routes>
  );
}
```

---

## 🔧 STEP 7: Error Handling

### Add Global Error Handler:
```javascript
// utils/api.js
export const handleApiError = (error) => {
  if (error.message.includes('401') || error.message.includes('token')) {
    // Token expired or invalid
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
  return error.message;
};
```

---

## ✅ QUICK CHECKLIST

Before your presentation, verify:

- [ ] `.env` file has correct API URL
- [ ] Login stores token and user in localStorage
- [ ] Register includes role field ('landlord' or 'tenant')
- [ ] getUserRole() returns user.profile.role
- [ ] Landlord dashboard shows "Add Property" button
- [ ] Tenant dashboard does NOT show "Add Property" button
- [ ] Properties API call includes Authorization header
- [ ] Create property only works for landlords
- [ ] Chat loads conversations with Authorization header
- [ ] Protected routes redirect if not authenticated

---

## 🧪 TEST YOUR FIXES

### Test 1: Registration
```javascript
// Register as landlord
{
  email: "landlord@test.com",
  password: "password123",
  first_name: "John",
  last_name: "Doe",
  role: "landlord"  // MUST include this
}

// Register as tenant
{
  email: "tenant@test.com",
  password: "password123",
  first_name: "Jane",
  last_name: "Smith",
  role: "tenant"  // MUST include this
}
```

### Test 2: Check Role After Login
```javascript
// In browser console after login
const user = JSON.parse(localStorage.getItem('user'));
console.log('User role:', user.profile.role);
// Should print: "landlord" or "tenant"
```

### Test 3: API Calls
```javascript
// In browser console
const token = localStorage.getItem('token');
console.log('Token:', token ? 'EXISTS' : 'MISSING');

// Test API call
fetch('https://landlord-app-backend-1eph.onrender.com/api/properties', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(console.log);
```

---

## 🆘 STILL NOT WORKING?

### Check Browser Console for:
1. CORS errors → Backend CORS_ORIGINS not set correctly
2. 401 errors → Token not being sent or invalid
3. 403 errors → User doesn't have permission (wrong role)
4. Network errors → API URL is wrong

### Check Network Tab:
1. Request URL should be: `https://landlord-app-backend-1eph.onrender.com/api/...`
2. Request Headers should include: `Authorization: Bearer <token>`
3. Response should be 200 OK (not 401, 403, or 500)

---

## 📞 Emergency Contact

If still broken before presentation:
1. Check Render logs for backend errors
2. Check browser console for frontend errors
3. Verify environment variables in Vercel
4. Test API with Postman to isolate frontend vs backend issues
