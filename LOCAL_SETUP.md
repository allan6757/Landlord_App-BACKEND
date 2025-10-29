# Local Development Setup Guide

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd Landlord_App-BACKEND
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python setup_database.py
```

### 3. Run Backend
```bash
python run.py
```

### 4. Run Frontend (separate terminal)
```bash
cd ../Landlord_App-FRONTEND
npm install
npm run dev
```

## ✅ Local Development Ready

The application is **fully configured** for local development:

### **Backend Configuration**:
- ✅ **Database**: SQLite (no PostgreSQL required locally)
- ✅ **Authentication**: JWT with local secrets
- ✅ **CORS**: Configured for localhost:3000
- ✅ **Optional Services**: Email/Cloudinary/MPesa work without API keys

### **Frontend Configuration**:
- ✅ **API URL**: Points to localhost:5000
- ✅ **Environment**: Development mode configured
- ✅ **Dependencies**: All required packages included

### **Sample Data Included**:
- **Landlord**: `landlord@example.com` / `password123`
- **Tenant**: `tenant@example.com` / `password123`
- **Admin**: `admin@example.com` / `admin123`

## 🔧 Local URLs

- **Backend API**: http://localhost:5000
- **Frontend App**: http://localhost:3000
- **Health Check**: http://localhost:5000/health

## 📋 Available Features Locally

### **Working Without External APIs**:
- ✅ User authentication and registration
- ✅ Property CRUD operations
- ✅ Chat/messaging system
- ✅ Dashboard statistics
- ✅ Payment records (without actual MPesa)
- ✅ User management

### **Requires API Keys (Optional)**:
- 📧 Email notifications (SendGrid)
- 🖼️ Image uploads (Cloudinary)
- 💳 Live payments (MPesa)

## 🚀 Test the Application

### 1. Backend Health Check
```bash
curl http://localhost:5000/health
```

### 2. Login Test
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"landlord@example.com","password":"password123"}' \
  http://localhost:5000/api/auth/login
```

### 3. Access Frontend
Open http://localhost:3000 in your browser

## 📁 Project Structure

```
Landlord_App-BACKEND/
├── app/                 # Flask application
├── .env                 # Local environment variables
├── landlord_app.db      # SQLite database (auto-created)
├── requirements.txt     # Python dependencies
├── run.py              # Application entry point
└── setup_database.py   # Database initialization

Landlord_App-FRONTEND/
├── src/                # React application
├── package.json        # Node dependencies
└── .env               # Frontend environment
```

## ✅ Ready to Run

The application is **100% ready** for local development with no additional setup required.