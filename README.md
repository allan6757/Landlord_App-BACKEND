# Landlord App Backend

A Flask-based REST API for a landlord-tenant management system.

## Features

- User authentication (landlords and tenants)
- Property management
- Payment tracking
- Chat messaging
- Role-based access control

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables in `.env`

3. Run the application:
```bash
python run.py
```

## API Endpoints

- `/api/auth/register` - User registration
- `/api/auth/login` - User login
- `/api/properties/` - Property management
- `/api/payments/` - Payment tracking
- `/api/chat/` - Messaging system
- `/api/users/` - User management