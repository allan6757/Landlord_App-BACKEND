# Quick Reference Guide

Quick commands and code snippets for common tasks.

## 🚀 Common Commands

### Virtual Environment
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deactivate
deactivate
```

### Running the App
```bash
# Development mode
python run.py

# Production mode
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history
```

### Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Add new dependency
pip install package-name
pip freeze > requirements.txt
```

## 📝 Code Snippets

### Creating a New API Resource

```python
# In app/resources/your_resource.py
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.your_model import YourModel
from app.schemas.your_schema import YourSchema
from app.utils.pagination import paginate_query
from app.utils.decorators import role_required
from flasgger import swag_from

your_schema = YourSchema()

class YourResourceList(Resource):
    @jwt_required()
    def get(self):
        """Get list with pagination"""
        query = YourModel.query
        result = paginate_query(query, your_schema)
        return result, 200
    
    @jwt_required()
    @role_required(UserRole.ADMIN)  # Restrict to specific role
    def post(self):
        """Create new item"""
        data = request.get_json()
        
        # Validate
        errors = your_schema.validate(data)
        if errors:
            return {'errors': errors}, 400
        
        try:
            # Create
            item = YourModel(**data)
            db.session.add(item)
            db.session.commit()
            
            return {'item': your_schema.dump(item)}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class YourResourceDetail(Resource):
    @jwt_required()
    def get(self, item_id):
        """Get single item"""
        item = YourModel.query.get_or_404(item_id)
        return {'item': your_schema.dump(item)}, 200
    
    @jwt_required()
    def put(self, item_id):
        """Update item"""
        item = YourModel.query.get_or_404(item_id)
        data = request.get_json()
        
        try:
            for key, value in data.items():
                setattr(item, key, value)
            
            db.session.commit()
            return {'item': your_schema.dump(item)}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
    
    @jwt_required()
    def delete(self, item_id):
        """Delete item"""
        item = YourModel.query.get_or_404(item_id)
        
        try:
            db.session.delete(item)
            db.session.commit()
            return {'message': 'Deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
```

### Creating a New Model

```python
# In app/models/your_model.py
from app import db
from app.models.base import BaseModel

class YourModel(BaseModel):
    """Description of your model"""
    __tablename__ = 'your_table_name'
    
    # Columns
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='your_items')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

### Creating a Marshmallow Schema

```python
# In app/schemas/your_schema.py
from marshmallow import Schema, fields, validate

class YourSchema(Schema):
    """Validation schema for YourModel"""
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
```

### Using RBAC Decorators

```python
from app.utils.decorators import role_required, landlord_required, admin_required
from app.models.user import UserRole

# Restrict to specific roles
@jwt_required()
@role_required(UserRole.ADMIN, UserRole.LANDLORD)
def some_function():
    pass

# Landlords only
@jwt_required()
@landlord_required
def landlord_function():
    pass

# Admins only
@jwt_required()
@admin_required
def admin_function():
    pass
```

### Sending Emails

```python
from app.utils.email_service import email_service

# Send verification email
email_service.send_verification_email(
    user_email='user@example.com',
    user_name='John Doe',
    verification_token='abc123'
)

# Send password reset email
email_service.send_password_reset_email(
    user_email='user@example.com',
    user_name='John Doe',
    reset_token='xyz789'
)

# Send payment confirmation
email_service.send_payment_confirmation(
    user_email='user@example.com',
    user_name='John Doe',
    payment_details={
        'amount': 50000,
        'property_name': 'Modern Apartment',
        'date': '2024-01-15',
        'transaction_id': 'TXN123'
    }
)
```

### Uploading Images

```python
from app.utils.cloudinary_service import cloudinary_service

# Upload property image
image_url = cloudinary_service.upload_property_image(
    image_file=request.files['image'],
    property_id=123
)

# Upload profile image
image_url = cloudinary_service.upload_profile_image(
    image_file=request.files['image'],
    user_id=456
)

# Delete image
success = cloudinary_service.delete_image(public_id='image_public_id')
```

### Using Pagination

```python
from app.utils.pagination import paginate_query, get_pagination_params

# Method 1: Using paginate_query helper
query = Property.query.filter_by(landlord_id=user_id)
result = paginate_query(query, property_schema)
return result, 200

# Method 2: Manual pagination
page, per_page = get_pagination_params()
paginated = query.paginate(page=page, per_page=per_page, error_out=False)
```

## 🔍 Testing with cURL

### Register User
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

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Get Profile (Protected Route)
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Property
```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Modern Apartment",
    "address": "123 Main St",
    "city": "Nairobi",
    "state": "Nairobi",
    "zip_code": "00100",
    "property_type": "apartment",
    "monthly_rent": 50000,
    "bedrooms": 2,
    "bathrooms": 2
  }'
```

### Upload Image
```bash
curl -X POST http://localhost:5000/api/properties/1/upload-image \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "image=@/path/to/image.jpg"
```

### Get List with Pagination
```bash
curl -X GET "http://localhost:5000/api/properties?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🐛 Debugging Tips

### Check Database Connection
```python
# In Python shell
from app import create_app, db
app = create_app()
with app.app_context():
    db.engine.connect()
    print("Database connected!")
```

### View All Routes
```bash
# In terminal
flask routes
```

### Check Environment Variables
```python
import os
print(os.environ.get('DATABASE_URL'))
print(os.environ.get('SENDGRID_API_KEY'))
```

### Test Email Service
```python
from app.utils.email_service import email_service
success = email_service.send_email(
    to_email='test@example.com',
    subject='Test Email',
    html_content='<h1>Test</h1>'
)
print(f"Email sent: {success}")
```

### Test Cloudinary Service
```python
from app.utils.cloudinary_service import cloudinary_service
print(f"Cloudinary configured: {cloudinary_service.is_configured()}")
```

## 📊 Database Queries

### Get User by Email
```python
from app.models.user import User
user = User.query.filter_by(email='test@example.com').first()
```

### Get Properties by Landlord
```python
from app.models.property import Property
properties = Property.query.filter_by(landlord_id=1).all()
```

### Get Payments with Joins
```python
from app.models.payment import Payment
from app.models.property import Property
payments = db.session.query(Payment).join(Property).filter(
    Property.landlord_id == 1
).all()
```

### Count Records
```python
from app.models.user import User
user_count = User.query.count()
```

## 🔐 Security Best Practices

### Password Hashing
```python
from app import bcrypt

# Hash password
hashed = bcrypt.generate_password_hash('password123').decode('utf-8')

# Check password
is_valid = bcrypt.check_password_hash(hashed, 'password123')
```

### Generate Secure Token
```python
import secrets
token = secrets.token_urlsafe(32)
```

### Validate JWT Token
```python
from flask_jwt_extended import get_jwt_identity, jwt_required

@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    # user_id is the ID from the token
```

## 📦 Git Workflow

### Feature Branch Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add your feature"

# Push to remote
git push origin feature/your-feature-name

# Create pull request on GitHub
# After review and approval, merge to develop
```

### Commit Message Convention
```bash
# Format: <type>: <description>

# Types:
feat: new feature
fix: bug fix
docs: documentation changes
style: formatting changes
refactor: code refactoring
test: adding tests
chore: maintenance tasks

# Examples:
git commit -m "feat: add email verification"
git commit -m "fix: resolve pagination bug"
git commit -m "docs: update README with setup instructions"
```

## 🚀 Deployment Commands

### Render Deployment
```bash
# Build command
pip install -r requirements.txt

# Start command
gunicorn run:app

# Or with workers
gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

### Database Migration on Render
```bash
# In Render shell
flask db upgrade
```

## 📱 Environment Variables Quick Reference

```env
# Required
SECRET_KEY=<random-string>
JWT_SECRET_KEY=<random-string>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SENDGRID_API_KEY=<sendgrid-key>
CLOUDINARY_CLOUD_NAME=<cloud-name>
CLOUDINARY_API_KEY=<api-key>
CLOUDINARY_API_SECRET=<api-secret>

# Optional
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
FLASK_ENV=development
```

---

**Pro Tip**: Bookmark this file for quick reference while developing! 🔖
