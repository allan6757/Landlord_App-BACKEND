#!/usr/bin/env python3
"""
Authentication system test and diagnostic script
"""

import os
import sys
import requests
import json
from pathlib import Path

# Set up environment
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = 'sqlite:///landlord_app.db'

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_backend_startup():
    """Test if backend can start properly"""
    try:
        from app import create_app, db
        from app.config import DevelopmentConfig
        
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            # Test database connection
            db.create_all()
            print("✅ Backend startup: SUCCESS")
            print("✅ Database connection: SUCCESS")
            return app
    except Exception as e:
        print(f"❌ Backend startup failed: {e}")
        return None

def test_sample_data():
    """Test if sample data exists"""
    try:
        from app.models import User
        from app import db
        
        users = User.query.all()
        if users:
            print(f"✅ Sample data: {len(users)} users found")
            for user in users:
                print(f"   - {user.email} ({user.role.value})")
        else:
            print("⚠️ No sample data found - creating...")
            create_sample_users()
        return True
    except Exception as e:
        print(f"❌ Sample data check failed: {e}")
        return False

def create_sample_users():
    """Create sample users for testing"""
    try:
        from app.models import User
        from app import db
        
        # Create test users
        landlord = User(
            email='landlord@example.com',
            first_name='John',
            last_name='Landlord',
            role='landlord'
        )
        landlord.set_password('password123')
        
        tenant = User(
            email='tenant@example.com',
            first_name='Jane',
            last_name='Tenant',
            role='tenant'
        )
        tenant.set_password('password123')
        
        db.session.add_all([landlord, tenant])
        db.session.commit()
        print("✅ Sample users created")
        
    except Exception as e:
        print(f"❌ Failed to create sample users: {e}")

def test_auth_endpoints():
    """Test authentication endpoints directly"""
    try:
        from app import create_app
        from app.config import DevelopmentConfig
        
        app = create_app(DevelopmentConfig)
        
        with app.test_client() as client:
            # Test login
            login_data = {
                "email": "landlord@example.com",
                "password": "password123"
            }
            
            response = client.post('/api/auth/login', 
                                 json=login_data,
                                 content_type='application/json')
            
            print(f"Login endpoint status: {response.status_code}")
            print(f"Login response: {response.get_json()}")
            
            if response.status_code == 200:
                print("✅ Login endpoint: SUCCESS")
                return response.get_json().get('token')
            else:
                print("❌ Login endpoint: FAILED")
                return None
                
    except Exception as e:
        print(f"❌ Auth endpoint test failed: {e}")
        return None

def test_registration():
    """Test user registration"""
    try:
        from app import create_app
        from app.config import DevelopmentConfig
        
        app = create_app(DevelopmentConfig)
        
        with app.test_client() as client:
            # Test registration
            register_data = {
                "email": "newuser@example.com",
                "password": "password123",
                "first_name": "New",
                "last_name": "User",
                "role": "tenant"
            }
            
            response = client.post('/api/auth/register', 
                                 json=register_data,
                                 content_type='application/json')
            
            print(f"Registration status: {response.status_code}")
            print(f"Registration response: {response.get_json()}")
            
            if response.status_code == 201:
                print("✅ Registration endpoint: SUCCESS")
                return True
            else:
                print("❌ Registration endpoint: FAILED")
                return False
                
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False

def main():
    """Run all authentication tests"""
    print("🔍 Authentication System Diagnostic")
    print("=" * 40)
    
    # Test backend startup
    app = test_backend_startup()
    if not app:
        return
    
    with app.app_context():
        # Test sample data
        test_sample_data()
        
        # Test authentication endpoints
        token = test_auth_endpoints()
        
        # Test registration
        test_registration()
    
    print("\n" + "=" * 40)
    print("🎯 Diagnostic Complete")
    
    if token:
        print("✅ Authentication system is working")
        print(f"🔑 Sample token: {token[:50]}...")
    else:
        print("❌ Authentication system has issues")

if __name__ == '__main__':
    main()