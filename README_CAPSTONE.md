# Rental Platform Backend - Capstone Project

A comprehensive property management REST API built with Flask, featuring JWT authentication, role-based access control, email verification, image uploads, and complete CRUD operations.

## 🎯 Capstone Requirements Compliance

### ✅ Technical Stack
- **Backend Framework**: Flask with Flask-RESTful
- **Database**: PostgreSQL (production-ready)
- **Serialization**: Marshmallow schemas
- **Authentication**: JWT (JSON Web Tokens)
- **RBAC**: Role-Based Access Control (Admin, Landlord, Tenant)
- **Email Service**: SendGrid integration
- **Image Handling**: Cloudinary with backend optimization
- **API Documentation**: Swagger/OpenAPI (Flasgger)
- **Pagination**: Implemented on all list endpoints

### ✅ Functional Requirements
- ✓ RESTful API with Flask-RESTful
- ✓ JWT Authentication
- ✓ RBAC with decorators (Admin, Landlord, Tenant roles)
- ✓ SendGrid email integration (verification, password reset)
- ✓ Cloudinary image uploads with optimization
- ✓ Complete CRUD operations for all models
- ✓ Pagination on all list endpoints
- ✓ Swagger API documentation
- ✓ 2-Step email verification (optional feature)

## 📋 Features

### 🔐 Authentication & Authorization
- User registration with email verification
- JWT-based authentication
- Role-based access control (RBAC)
- Password reset via email
- Protected routes with decorators

### 🏠 Property Management
- Create, read, update, delete properties (CRUD)
- Image upload with Cloudinary
- Role-based property filtering
- Pagination support
- Landlord-only property creation

### 💰 Payment System
- Payment tracking and history
- M-Pesa integration support
- Payment confirmation emails
- Role-based payment access

### 💬 Chat System
- Real-time messaging between landlords and tenants
- Conversation management
- Message history

### 📧 Email Notifications
- Email verification for new users
- Password reset emails
- Payment confirmation emails
- SendGrid integration

### 🖼️ Image Management
- Property image uploads
- Profile picture uploads
- Backend image optimization (resize, compress)
- Cloudinary CDN integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- SendGrid account (for emails)
- Cloudinary account (for images)

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Landlord_App-BACKEND

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
FLASK_ENV=development

# Database Configuration (PostgreSQL required)
DATABASE_URL=postgresql://username:password@localhost:5432/rental_platform

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com

# SendGrid Email Configuration (REQUIRED)
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=noreply@yourdomain.com

# Cloudinary Configuration (REQUIRED)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:3000

# Optional: M-Pesa Configuration
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=your-passkey
```

### 3. Database Setup

```bash
# Initialize database
flask db init

# Create migrations
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade

# Optional: Load sample data
python setup_database.py
```

### 4. Run the Application

```bash
# Development mode
python run.py

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Swagger UI
Access interactive API documentation at: `http://localhost:5000/api/docs`

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### Get Profile
```http
GET /api/auth/profile
Authorization: Bearer <your-jwt-token>
```

#### Send Verification Email
```http
POST /api/auth/send-verification
Authorization: Bearer <your-jwt-token>
```

#### Verify Email
```http
POST /api/auth/verify-email
Content-Type: application/json

{
  "token": "verification-token-from-email"
}
```

### Property Endpoints

#### List Properties (with pagination)
```http
GET /api/properties?page=1&per_page=10
Authorization: Bearer <your-jwt-token>
```

#### Create Property (Landlords only)
```http
POST /api/properties
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "title": "Modern Apartment",
  "description": "Beautiful 2BR apartment",
  "address": "123 Main St",
  "city": "Nairobi",
  "state": "Nairobi",
  "zip_code": "00100",
  "property_type": "apartment",
  "monthly_rent": 50000,
  "bedrooms": 2,
  "bathrooms": 2
}
```

#### Upload Property Image
```http
POST /api/properties/{property_id}/upload-image
Authorization: Bearer <your-jwt-token>
Content-Type: multipart/form-data

image: <file>
```

#### Get Property Details
```http
GET /api/properties/{property_id}
Authorization: Bearer <your-jwt-token>
```

#### Update Property
```http
PUT /api/properties/{property_id}
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "monthly_rent": 55000,
  "status": "occupied"
}
```

#### Delete Property
```http
DELETE /api/properties/{property_id}
Authorization: Bearer <your-jwt-token>
```

### Payment Endpoints

#### List Payments (with pagination)
```http
GET /api/payments?page=1&per_page=10
Authorization: Bearer <your-jwt-token>
```

#### Create Payment
```http
POST /api/payments
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "property_id": 1,
  "amount": 50000,
  "payment_method": "mpesa"
}
```

## 🗄️ Database Schema

### Users & Profiles
- **users**: Basic authentication (email, password, name)
- **user_profiles**: Extended info (phone, address, role, DOB)

### Properties
- **properties**: Property details, rent, location, amenities

### Payments
- **payments**: Transaction history, amounts, status

### Chat
- **chat_conversations**: Conversation threads
- **chat_messages**: Individual messages

### Verification
- **verification_tokens**: Email verification and password reset tokens

## 🔒 Role-Based Access Control (RBAC)

### Roles
1. **Admin**: Full system access
2. **Landlord**: Manage properties, view payments, chat with tenants
3. **Tenant**: View assigned properties, make payments, chat with landlords

### RBAC Decorators
```python
from app.utils.decorators import role_required, landlord_required, admin_required

# Restrict to specific roles
@role_required(UserRole.ADMIN, UserRole.LANDLORD)
def some_function():
    pass

# Landlords only
@landlord_required
def landlord_function():
    pass

# Admins only
@admin_required
def admin_function():
    pass
```

## 📦 Project Structure

```
Landlord_App-BACKEND/
├── app/
│   ├── __init__.py              # App factory and configuration
│   ├── config.py                # Configuration classes
│   ├── swagger_config.py        # Swagger/OpenAPI configuration
│   ├── models/                  # Database models
│   │   ├── user.py              # User and UserProfile models
│   │   ├── property.py          # Property model
│   │   ├── payment.py           # Payment model
│   │   ├── chat.py              # Chat models
│   │   └── verification.py      # Email verification tokens
│   ├── resources/               # API endpoints (Flask-RESTful)
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── email_verification.py # Email verification endpoints
│   │   ├── images.py            # Image upload endpoints
│   │   ├── properties.py        # Property CRUD
│   │   ├── payments.py          # Payment management
│   │   ├── users.py             # User management
│   │   └── chat.py              # Chat endpoints
│   ├── schemas/                 # Marshmallow schemas
│   │   ├── user.py
│   │   ├── property.py
│   │   └── payment.py
│   └── utils/                   # Utility functions
│       ├── decorators.py        # RBAC decorators
│       ├── pagination.py        # Pagination helper
│       ├── email_service.py     # SendGrid integration
│       ├── cloudinary_service.py # Cloudinary integration
│       └── validators.py        # Custom validators
├── migrations/                  # Database migrations
├── tests/                       # Unit tests
├── .env                         # Environment variables (not in git)
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🚢 Deployment

### Render Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables in Render dashboard
4. Deploy!

```yaml
# render.yaml
services:
  - type: web
    name: rental-platform-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: rental-platform-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
```

### Environment Variables Checklist
- [ ] SECRET_KEY
- [ ] JWT_SECRET_KEY
- [ ] DATABASE_URL (PostgreSQL)
- [ ] SENDGRID_API_KEY
- [ ] SENDGRID_FROM_EMAIL
- [ ] CLOUDINARY_CLOUD_NAME
- [ ] CLOUDINARY_API_KEY
- [ ] CLOUDINARY_API_SECRET
- [ ] FRONTEND_URL
- [ ] CORS_ORIGINS

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 📝 API Best Practices Implemented

1. **RESTful Design**: Proper HTTP methods and status codes
2. **Error Handling**: Consistent error responses with meaningful messages
3. **Validation**: Input validation using Marshmallow schemas
4. **Pagination**: All list endpoints support pagination
5. **Authentication**: JWT tokens with proper expiration
6. **Authorization**: Role-based access control
7. **Documentation**: Swagger/OpenAPI documentation
8. **Security**: Password hashing, CORS configuration, input sanitization

## 🔧 Development Tips

### Database Migrations
```bash
# Create new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade
```

### Testing Email Locally
Use SendGrid's sandbox mode or a service like Mailtrap for testing emails without sending real emails.

### Testing Image Uploads
Ensure Cloudinary credentials are set. Images are automatically optimized before upload.

## 📞 Support

For issues or questions:
- Check the Swagger documentation at `/api/docs`
- Review the code comments (well-documented for learning)
- Check environment variables configuration

## 🎓 Learning Resources

This project demonstrates:
- Flask application factory pattern
- RESTful API design
- Database relationships and migrations
- JWT authentication
- Role-based authorization
- Third-party service integration (SendGrid, Cloudinary)
- Error handling and validation
- API documentation with Swagger

## 📄 License

This project is for educational purposes as part of a bootcamp capstone project.

---

**Built with ❤️ for Capstone Project**
