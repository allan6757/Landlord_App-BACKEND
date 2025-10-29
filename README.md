# Rental Platform Backend - Complete MVP

A comprehensive property management system backend built with Flask-RESTful, providing complete REST APIs for landlords and tenants to manage properties, payments, and communications.

## ✅ Fully Implemented MVP Features

### 🔐 **Complete Authentication System**
- JWT-based authentication with Flask-JWT-Extended
- Secure password hashing with Werkzeug
- Role-based access control (landlord/tenant/admin)
- User registration with email validation
- Profile management with image upload
- Welcome email notifications

### 💬 **Full Chat/Messaging System**
- Real-time messaging between landlords and tenants
- Property-specific conversations
- Message read status tracking
- Conversation management (create, list, delete)
- Unread message counts for dashboards

### 📊 **Complete Dashboard Implementation**
- **Landlord Dashboard**: Property stats, revenue tracking, recent payments
- **Tenant Dashboard**: Property details, payment history, rent due dates
- Real-time statistics and activity feeds
- Unread message notifications

### 💳 **Working Payment Integration**
- Full MPesa STK Push integration
- Payment status tracking (pending/completed/failed)
- Payment history and reporting
- Email confirmations for completed payments
- Landlord payment management

### ☁️ **Complete Cloudinary Integration**
- Property image upload and management
- User profile image upload
- Automatic image optimization and resizing
- Secure image deletion

### 🏠 **Full Property Management**
- Complete CRUD operations for properties
- Property status management (available/occupied/maintenance)
- Landlord-tenant property relationships
- Property image galleries
- Advanced property filtering

### 📦 **Production-Ready Configuration**
- PostgreSQL database (required for capstone)
- Proper package dependencies
- Environment-based configuration
- Email service integration (SendGrid)
- Production deployment ready

## Tech Stack Compliance

✅ **Backend**: Flask-RESTful for building APIs  
✅ **Serialization**: Marshmallow for data validation  
✅ **Database**: PostgreSQL (SQLite not allowed)  
✅ **File Upload**: Cloudinary integration  
✅ **Payment**: MPesa integration  
✅ **Email**: SendGrid integration  

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create `.env` file with your credentials:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://user:password@localhost:5432/rental_platform

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# MPesa
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=your-passkey

# SendGrid
SENDGRID_API_KEY=your-sendgrid-key
SENDGRID_FROM_EMAIL=noreply@yourapp.com
```

### 3. Database Setup
```bash
python setup_database.py
```

### 4. Run Application
```bash
python run.py
```

## Complete API Endpoints

### Authentication
- `POST /api/auth/register` - User registration with email
- `POST /api/auth/login` - User login with JWT
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Properties
- `GET /api/properties` - List properties (role-filtered)
- `POST /api/properties` - Create property (landlords only)
- `GET /api/properties/{id}` - Get property details
- `PUT /api/properties/{id}` - Update property
- `DELETE /api/properties/{id}` - Delete property
- `POST /api/properties/{id}/images` - Upload property images

### Payments
- `GET /api/payments` - List payments (role-filtered)
- `POST /api/payments` - Create payment with MPesa
- `GET /api/payments/{id}` - Get payment details
- `PUT /api/payments/{id}` - Update payment status
- `POST /api/payments/callback` - MPesa callback handler

### Chat System
- `GET /api/conversations` - List conversations
- `POST /api/conversations` - Start new conversation
- `GET /api/conversations/{id}` - Get conversation details
- `DELETE /api/conversations/{id}` - Delete conversation
- `GET /api/conversations/{id}/messages` - Get messages
- `POST /api/conversations/{id}/messages` - Send message

### Dashboards
- `GET /api/dashboard/landlord` - Landlord dashboard with stats
- `GET /api/dashboard/tenant` - Tenant dashboard with stats

### Users
- `GET /api/users` - List users (admin only)
- `GET /api/users/{id}` - Get user details
- `POST /api/users/profile-image` - Upload profile image

## Database Schema

### Core Tables
1. **users** - User authentication and profiles
2. **properties** - Property details with images
3. **payments** - Payment transactions with MPesa
4. **chat_conversations** - Conversation threads
5. **chat_messages** - Individual messages

### Role-Based Access
- **Landlords**: Manage properties, view payments, chat with tenants
- **Tenants**: View assigned properties, make payments, chat with landlords
- **Admins**: Full system access

## Sample Data

The setup script creates sample accounts:
- **Landlord**: `landlord@example.com` / `password123`
- **Tenant**: `tenant@example.com` / `password123`
- **Admin**: `admin@example.com` / `admin123`

## Production Features

✅ **Security**: JWT authentication, password hashing, CORS  
✅ **File Upload**: Cloudinary integration with optimization  
✅ **Payments**: MPesa STK Push with callbacks  
✅ **Email**: SendGrid integration for notifications  
✅ **Database**: PostgreSQL with proper relationships  
✅ **Validation**: Marshmallow schemas for all endpoints  
✅ **Error Handling**: Comprehensive error responses  
✅ **Documentation**: Complete API documentation  

## Deployment

### Environment Variables Required
- `DATABASE_URL` - PostgreSQL connection string
- `CLOUDINARY_*` - Cloudinary credentials
- `MPESA_*` - MPesa API credentials
- `SENDGRID_*` - SendGrid email credentials

### Production Deployment
```bash
gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

This backend provides a complete, production-ready foundation for a property management platform with all essential MVP features fully implemented and tested.