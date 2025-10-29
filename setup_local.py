#!/usr/bin/env python3
"""
Local development setup script
Creates database and demo users
"""

import os
import sys
from pathlib import Path

# Set environment for local development
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = 'sqlite:///landlord_app.db'

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def setup_database():
    """Setup database and create demo users"""
    try:
        from app import create_app, db
        from app.config import DevelopmentConfig
        from app.models import User
        
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created")
            
            # Check if demo user exists
            demo_user = User.query.filter_by(email='demouser@example.com').first()
            if demo_user:
                print("✅ Demo user already exists")
            else:
                # Create demo user
                demo_user = User(
                    email='demouser@example.com',
                    first_name='Demo',
                    last_name='User',
                    role='tenant'
                )
                demo_user.set_password('demo123')
                db.session.add(demo_user)
                
                # Create landlord demo user
                demo_landlord = User(
                    email='demolandlord@example.com',
                    first_name='Demo',
                    last_name='Landlord',
                    role='landlord'
                )
                demo_landlord.set_password('demo123')
                db.session.add(demo_landlord)
                
                db.session.commit()
                print("✅ Demo users created")
            
            # Verify users exist
            users = User.query.all()
            print(f"✅ Total users in database: {len(users)}")
            for user in users:
                print(f"   - {user.email} ({user.role})")
            
            return True
            
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_authentication():
    """Test authentication endpoints"""
    try:
        from app import create_app
        from app.config import DevelopmentConfig
        
        app = create_app(DevelopmentConfig)
        
        with app.test_client() as client:
            # Test login with demo credentials
            response = client.post('/api/auth/login', 
                                 json={'email': 'demouser@example.com', 'password': 'demo123'},
                                 content_type='application/json')
            
            print(f"Login test - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print("✅ Login successful")
                print(f"   Token: {data.get('token', 'N/A')[:50]}...")
                return True
            else:
                print(f"❌ Login failed: {response.get_json()}")
                return False
                
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🔧 Setting up local development environment...")
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    # Test authentication
    if not test_authentication():
        sys.exit(1)
    
    print("\n🚀 Setup complete!")
    print("Demo credentials:")
    print("  Tenant: demouser@example.com / demo123")
    print("  Landlord: demolandlord@example.com / demo123")
    print("\nTo start the server: python run.py")

if __name__ == '__main__':
    main()