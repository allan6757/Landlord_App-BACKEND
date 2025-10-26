# Rental Platform Backend

A comprehensive property management system backend built with Flask, providing REST APIs for landlords and tenants to manage properties, payments, and communications.

## Features

### 🏠 **Complete Database Schema**
- **Users & Profiles**: Extended user system with role-based access (landlord/tenant/admin)
- **Properties**: Full property management with occupancy tracking
- **Payments**: Complete payment transaction history with M-Pesa integration
- **Chat System**: Real-time messaging between landlords and tenants

### 🔐 **Security & Authentication**
- JWT-based authentication with role-based access control
- Password hashing with bcrypt
- Row-level security through proper data access patterns
- CORS configuration for frontend integration

### 📡 **REST API Endpoints**

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

#### Properties
- `GET /api/properties` - List properties (filtered by user role)
- `POST /api/properties` - Create property (landlords only)
- `GET /api/properties/{id}` - Get property details
- `PUT /api/properties/{id}` - Update property
- `DELETE /api/properties/{id}` - Delete property

#### Payments
- `GET /api/payments` - List payments (role-filtered)
- `POST /api/payments` - Create payment
- `GET /api/payments/{id}` - Get payment details
- `PUT /api/payments/{id}` - Update payment status

#### Chat System
- `GET /api/conversations` - List conversations
- `POST /api/conversations` - Start new conversation
- `GET /api/conversations/{id}` - Get conversation details
- `GET /api/conversations/{id}/messages` - Get messages
- `POST /api/conversations/{id}/messages` - Send message

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create `.env` file:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://rental_user:rental_password@localhost:5432/rental_platform
```

### 3. Database Setup
```bash
# Setup database and sample data
python setup_database.py
```

### 4. Run Application
```bash
python run.py
```

## Database Schema

### Core Tables
1. **users** - Basic user authentication
2. **user_profiles** - Extended user information with roles
3. **properties** - Property details and occupancy
4. **payments** - Payment transactions with M-Pesa support
5. **chat_conversations** - Conversation threads
6. **chat_messages** - Individual messages

### Role-Based Access
- **Landlords**: Manage their properties, view payments, chat with tenants
- **Tenants**: View assigned properties, make payments, chat with landlords
- **Admins**: Full system access

## API Authentication

All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Sample Data

The setup script creates sample accounts:
- **Landlord**: `landlord@example.com` / `password123`
- **Tenant**: `tenant@example.com` / `password123`

## Production Deployment

1. Set environment variables for production
2. Configure PostgreSQL database
3. Set up M-Pesa credentials for payments
4. Configure email settings for notifications
5. Use gunicorn for production server

## Architecture Benefits

✅ **Complete CRUD Operations** for all entities
✅ **Role-Based Security** with proper access control
✅ **Payment Integration** with M-Pesa support
✅ **Real-Time Chat** system for communication
✅ **Database Migrations** for schema management
✅ **Production Ready** with proper configuration
✅ **Comprehensive Testing** structure included

This backend provides a solid foundation for a property management platform with all the essential features for landlords and tenants to manage their rental relationships effectively.