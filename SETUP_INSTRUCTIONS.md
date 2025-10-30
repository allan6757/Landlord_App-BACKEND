# PropManager Property Management System - Setup Instructions

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (production) or SQLite (development)
- M-Pesa Daraja API credentials (optional for testing)

### Installation Steps

#### 1. Clone and Navigate to Project
```bash
cd "land_App backend/Landlord_App-BACKEND"
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database (SQLite for development)
DATABASE_URL=sqlite:///landlord_app.db

# CORS (React frontend URL)
CORS_ORIGINS=http://localhost:3000

# M-Pesa Configuration (Optional - for payment testing)
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=your_passkey

# Email Configuration (Optional)
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=noreply@yourapp.com

# Cloudinary Configuration (Optional - for image uploads)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

#### 5. Initialize Database
```bash
# Create database tables
python init_db.py

# Or use Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 6. Run Development Server
```bash
# Start Flask server
python run.py

# Server will start on http://localhost:5000
```

---

## 📡 API Endpoints

### Authentication Endpoints

#### Register New User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe",
  "role": "tenant"  // or "landlord"
}

# Response:
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "profile": {
      "id": 1,
      "role": "tenant"
    }
  }
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

# Response: Same as register
```

#### Get Profile
```bash
GET /api/auth/profile
Authorization: Bearer <your_jwt_token>

# Response:
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "profile": {
      "id": 1,
      "role": "tenant"
    }
  }
}
```

### Property Endpoints

#### List Properties
```bash
GET /api/properties
Authorization: Bearer <your_jwt_token>

# Response:
{
  "properties": [
    {
      "id": 1,
      "title": "Modern Apartment",
      "monthly_rent": 1500.00,
      "status": "occupied",  // or "vacant"
      "landlord_id": 2,
      "tenant_id": 3,
      "address": "123 Main St",
      "city": "Nairobi"
    }
  ]
}
```

#### Create Property (Landlord Only)
```bash
POST /api/properties
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "title": "Modern Apartment",
  "address": "123 Main St",
  "city": "Nairobi",
  "state": "Nairobi",
  "zip_code": "00100",
  "property_type": "apartment",
  "monthly_rent": 1500.00,
  "bedrooms": 2,
  "bathrooms": 1,
  "status": "vacant"
}
```

### Payment Endpoints

#### List Payments
```bash
GET /api/payments
Authorization: Bearer <your_jwt_token>

# Response:
{
  "payments": [
    {
      "id": 1,
      "amount": 1500.00,
      "status": "completed",  // pending/completed/failed
      "due_date": "2024-01-15T00:00:00",
      "property": {...},
      "tenant": {...}
    }
  ]
}
```

#### Create Payment with M-Pesa STK Push
```bash
POST /api/payments
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "property_id": 1,
  "amount": 1500.00,
  "phone_number": "254712345678",  // Kenyan phone format
  "payment_method": "mpesa"
}

# This will:
# 1. Create payment record
# 2. Send STK Push to user's phone
# 3. User enters M-Pesa PIN
# 4. M-Pesa sends callback to /api/payments/callback
# 5. Payment status updated to 'completed' or 'failed'
```

### Chat Endpoints

#### List Conversations
```bash
GET /api/conversations
Authorization: Bearer <your_jwt_token>

# Response:
{
  "conversations": [
    {
      "id": 1,
      "initiator_id": 2,      // sender_id
      "participant_id": 3,    // receiver_id
      "property_id": 1,
      "last_message": "Hello",
      "last_message_at": "2024-01-15T10:30:00"
    }
  ]
}
```

#### Create Conversation
```bash
POST /api/conversations
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "participant_id": 3,  // User to chat with
  "property_id": 1      // Optional: Related property
}
```

#### Get Messages
```bash
GET /api/conversations/1/messages
Authorization: Bearer <your_jwt_token>

# Response:
{
  "messages": [
    {
      "id": 1,
      "sender_id": 2,
      "content": "Hello, is the property available?",
      "timestamp": "2024-01-15T10:30:00",
      "is_read": false
    }
  ]
}
```

#### Send Message
```bash
POST /api/conversations/1/messages
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "content": "Hello, is the property available?"
}
```

---

## 🔐 Authentication

All protected endpoints require JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

Token is returned from `/api/auth/register` and `/api/auth/login` endpoints.

Store the token in your frontend (localStorage or cookies) and include it in all API requests.

---

## 👥 Role-Based Access Control

### Landlord Role
- Can create properties
- Can view their own properties
- Can view payments for their properties
- Can update payment status
- Can chat with tenants

### Tenant Role
- Can view assigned properties
- Can make payments for assigned properties
- Can view their own payments
- Can chat with landlords

---

## 💳 M-Pesa Integration Setup

### 1. Register for M-Pesa Daraja API
1. Go to https://developer.safaricom.co.ke
2. Create an account
3. Create a new app
4. Get Consumer Key and Consumer Secret

### 2. Configure M-Pesa Credentials
Add to `.env` file:
```env
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
```

### 3. Set Callback URL
Update callback URL in `app/utils/mpesa.py`:
```python
self.callback_url = 'https://yourdomain.com/api/payments/callback'
```

### 4. Testing M-Pesa
- Use Safaricom sandbox for testing
- Test phone numbers: 254708374149, 254712345678
- Sandbox URL: https://sandbox.safaricom.co.ke

---

## 🗄️ Database Models

### User Model
```python
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "profile": {
    "id": 1,
    "role": "tenant"  // or "landlord"
  }
}
```

### Property Model
```python
{
  "id": 1,
  "title": "Modern Apartment",
  "monthly_rent": 1500.00,
  "status": "occupied",  // or "vacant"
  "landlord_id": 2,
  "tenant_id": 3
}
```

### Payment Model
```python
{
  "id": 1,
  "amount": 1500.00,
  "status": "completed",  // pending/completed/failed
  "due_date": "2024-01-15T00:00:00",
  "property_id": 1
}
```

### Message Model
```python
{
  "id": 1,
  "sender_id": 2,
  "receiver_id": 3,
  "content": "Hello",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 🧪 Testing

### Test Authentication
```bash
# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","role":"tenant"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### Test Properties
```bash
# Get properties (requires token)
curl -X GET http://localhost:5000/api/properties \
  -H "Authorization: Bearer <your_token>"
```

### Run Unit Tests
```bash
pytest tests/
```

---

## 🚀 Production Deployment

### Using Gunicorn
```bash
gunicorn --worker-class eventlet -w 1 run:app
```

### Using Docker
```bash
docker build -t propmanager-api .
docker run -p 5000:5000 propmanager-api
```

### Environment Variables for Production
```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:5432/dbname
CORS_ORIGINS=https://yourfrontend.com
```

---

## 📝 Frontend Integration

### React Example
```javascript
// Login
const login = async (email, password) => {
  const response = await fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data.user;
};

// Get properties
const getProperties = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:5000/api/properties', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const data = await response.json();
  return data.properties;
};

// Create payment
const createPayment = async (propertyId, amount, phoneNumber) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:5000/api/payments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      property_id: propertyId,
      amount: amount,
      phone_number: phoneNumber,
      payment_method: 'mpesa'
    })
  });
  return await response.json();
};
```

---

## 🔧 Troubleshooting

### Database Connection Error
```bash
# Reset database
rm instance/landlord_app.db
python init_db.py
```

### CORS Error
Check `CORS_ORIGINS` in `.env` matches your frontend URL:
```env
CORS_ORIGINS=http://localhost:3000
```

### JWT Token Error
Ensure token is included in Authorization header:
```
Authorization: Bearer <token>
```

### M-Pesa Error
- Verify credentials in `.env`
- Check phone number format: 254XXXXXXXXX
- Ensure callback URL is publicly accessible

---

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io
- M-Pesa Daraja API: https://developer.safaricom.co.ke
- SQLAlchemy: https://www.sqlalchemy.org

---

## 🤝 Support

For issues or questions, please check:
1. This documentation
2. Code comments in source files
3. Error logs in console output
