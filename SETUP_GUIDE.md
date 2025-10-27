# Setup Guide - Rental Platform Backend

This guide will help you set up the backend from scratch. Follow these steps carefully.

## 📋 Prerequisites

Before you begin, make sure you have:

1. **Python 3.8 or higher** installed
   ```bash
   python --version  # Should show 3.8+
   ```

2. **PostgreSQL** installed and running
   ```bash
   psql --version  # Should show PostgreSQL version
   ```

3. **Git** installed
   ```bash
   git --version
   ```

4. **SendGrid Account** (free tier is fine)
   - Sign up at: https://sendgrid.com/
   - Get your API key from Settings > API Keys

5. **Cloudinary Account** (free tier is fine)
   - Sign up at: https://cloudinary.com/
   - Get your credentials from Dashboard

## 🚀 Step-by-Step Setup

### Step 1: Clone and Navigate

```bash
# Clone your repository
git clone <your-repo-url>
cd Landlord_App-BACKEND
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This will install:
# - Flask and extensions
# - PostgreSQL driver
# - Marshmallow for serialization
# - SendGrid for emails
# - Cloudinary for images
# - Swagger for API docs
# - And more...
```

### Step 4: Set Up PostgreSQL Database

```bash
# Open PostgreSQL command line
psql postgres

# Create database and user
CREATE DATABASE rental_platform;
CREATE USER rental_user WITH PASSWORD 'rental_password';
GRANT ALL PRIVILEGES ON DATABASE rental_platform TO rental_user;

# Exit psql
\q
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your actual values
nano .env  # or use any text editor
```

**Important**: Fill in these values in your `.env` file:

```env
# Flask Configuration
SECRET_KEY=your-random-secret-key-here-make-it-long-and-random
JWT_SECRET_KEY=another-random-secret-key-for-jwt-tokens
FLASK_ENV=development

# Database (use the credentials you created above)
DATABASE_URL=postgresql://rental_user:rental_password@localhost:5432/rental_platform

# CORS (your frontend URL)
CORS_ORIGINS=http://localhost:3000

# SendGrid (get from SendGrid dashboard)
SENDGRID_API_KEY=SG.your-sendgrid-api-key-here
SENDGRID_FROM_EMAIL=noreply@yourdomain.com

# Cloudinary (get from Cloudinary dashboard)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:3000
```

**How to get SendGrid API Key:**
1. Go to https://app.sendgrid.com/
2. Navigate to Settings > API Keys
3. Click "Create API Key"
4. Give it a name and select "Full Access"
5. Copy the key (you won't see it again!)

**How to get Cloudinary credentials:**
1. Go to https://cloudinary.com/console
2. Your credentials are on the dashboard:
   - Cloud Name
   - API Key
   - API Secret

### Step 6: Initialize Database

```bash
# Initialize Flask-Migrate
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations to database
flask db upgrade

# Optional: Load sample data
python setup_database.py
```

### Step 7: Run the Application

```bash
# Start the development server
python run.py

# You should see:
# * Running on http://0.0.0.0:5000
# * Debug mode: on
```

### Step 8: Test the API

Open your browser and go to:
- **Health Check**: http://localhost:5000/health
- **API Documentation**: http://localhost:5000/api/docs

You should see the Swagger UI with all API endpoints!

## 🧪 Testing the Setup

### Test 1: Register a User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

You should get a response with an access token!

### Test 2: Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test 3: Access Protected Route

```bash
# Replace <TOKEN> with the token from login response
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer <TOKEN>"
```

## 🔧 Common Issues and Solutions

### Issue 1: "ModuleNotFoundError"
**Solution**: Make sure virtual environment is activated and dependencies are installed
```bash
source venv/bin/activate  # Activate venv
pip install -r requirements.txt  # Reinstall dependencies
```

### Issue 2: "Database connection error"
**Solution**: Check PostgreSQL is running and credentials are correct
```bash
# Check if PostgreSQL is running
sudo service postgresql status  # Linux
brew services list  # macOS

# Test database connection
psql -U rental_user -d rental_platform
```

### Issue 3: "SendGrid authentication failed"
**Solution**: Verify your SendGrid API key is correct
- Check the key in your `.env` file
- Make sure there are no extra spaces
- Verify the key is active in SendGrid dashboard

### Issue 4: "Cloudinary upload failed"
**Solution**: Verify Cloudinary credentials
- Check all three values (cloud_name, api_key, api_secret)
- Make sure they match your Cloudinary dashboard

### Issue 5: "Port 5000 already in use"
**Solution**: Kill the process using port 5000 or use a different port
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or change port in run.py
```

## 📚 Next Steps

After successful setup:

1. **Explore the API**: Use Swagger UI at http://localhost:5000/api/docs
2. **Read the Code**: All files are well-commented for learning
3. **Test Features**: Try creating properties, uploading images, etc.
4. **Connect Frontend**: Update CORS_ORIGINS with your frontend URL
5. **Deploy**: Follow DEPLOYMENT.md for production deployment

## 🎓 Understanding the Project Structure

```
app/
├── __init__.py           # App factory - creates and configures Flask app
├── config.py             # Configuration for dev/prod environments
├── models/               # Database models (tables)
│   ├── user.py          # User and UserProfile models
│   ├── property.py      # Property model
│   ├── payment.py       # Payment model
│   └── verification.py  # Email verification tokens
├── resources/            # API endpoints (like controllers)
│   ├── auth.py          # Login, register, profile
│   ├── properties.py    # Property CRUD operations
│   └── ...
├── schemas/              # Data validation (Marshmallow)
│   ├── user.py          # User validation rules
│   └── ...
└── utils/                # Helper functions
    ├── decorators.py    # RBAC decorators
    ├── pagination.py    # Pagination helper
    ├── email_service.py # SendGrid integration
    └── cloudinary_service.py # Image uploads
```

## 💡 Tips for Learning

1. **Start with auth.py**: Understand how registration and login work
2. **Check decorators.py**: See how RBAC is implemented
3. **Read models**: Understand database relationships
4. **Test with Swagger**: Interactive API testing
5. **Read comments**: Every file has detailed comments explaining the code

## 🆘 Getting Help

If you're stuck:
1. Check the error message carefully
2. Look at the relevant code file (they're well-commented)
3. Check the Swagger docs for correct API usage
4. Verify environment variables are set correctly
5. Make sure database migrations are applied

## ✅ Setup Checklist

- [ ] Python 3.8+ installed
- [ ] PostgreSQL installed and running
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] PostgreSQL database created
- [ ] `.env` file created with all variables
- [ ] SendGrid API key configured
- [ ] Cloudinary credentials configured
- [ ] Database migrations applied (`flask db upgrade`)
- [ ] Application runs successfully (`python run.py`)
- [ ] Health check works (http://localhost:5000/health)
- [ ] Swagger docs accessible (http://localhost:5000/api/docs)
- [ ] Test user registration works

Once all items are checked, you're ready to develop! 🎉

---

**Need more help?** Check README_CAPSTONE.md for detailed API documentation.
