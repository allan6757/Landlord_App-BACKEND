#!/usr/bin/env python3
"""
Database setup script for Rental Platform
Creates tables and sample data
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

def create_sample_data():
    """Create sample users and data for testing"""
    from app.models import User, Property, Payment, Conversation, Message
    from app import db
    from datetime import datetime, date
    
    # Check if data already exists
    if User.query.first():
        print("⚠️  Sample data already exists. Skipping creation.")
        return
    
    print("📝 Creating sample data...")
    
    # Create sample landlord
    landlord = User(
        email='landlord@example.com',
        first_name='John',
        last_name='Landlord',
        phone='+254700000001',
        role='landlord'
    )
    landlord.set_password('password123')
    
    # Create sample tenant
    tenant = User(
        email='tenant@example.com',
        first_name='Jane',
        last_name='Tenant',
        phone='+254700000002',
        role='tenant'
    )
    tenant.set_password('password123')
    
    # Create admin user
    admin = User(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        phone='+254700000000',
        role='admin'
    )
    admin.set_password('admin123')
    
    db.session.add_all([landlord, tenant, admin])
    db.session.commit()
    
    print("✅ Sample users created")
    print("\n🔑 Test Accounts:")
    print("   Landlord: landlord@example.com / password123")
    print("   Tenant: tenant@example.com / password123")
    print("   Admin: admin@example.com / admin123")

def main():
    """Main setup function"""
    try:
        from app import create_app, db
        from app.config import DevelopmentConfig
        
        print("🔧 Setting up database...")
        
        app = create_app(DevelopmentConfig)
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created!")
            
            # Create sample data
            create_sample_data()
            
        print("\n🚀 Database setup complete!")
        print("You can now run: python run_local.py")
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)