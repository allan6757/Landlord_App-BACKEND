#!/usr/bin/env python3
"""
Production database initialization
Creates tables and demo users for production
"""

import os
from app import create_app, db
from app.config import ProductionConfig

def init_production_database():
    """Initialize production database with demo users"""
    app = create_app(ProductionConfig)
    
    with app.app_context():
        try:
            # Import all models to ensure they're registered
            from app.models import User, Property, Payment, Conversation, Message
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created")
            
            # Check if demo users exist
            if not User.query.filter_by(email='landlord@example.com').first():
                # Create demo landlord
                landlord = User(
                    email='landlord@example.com',
                    first_name='John',
                    last_name='Landlord',
                    role='landlord'
                )
                landlord.set_password('password123')
                db.session.add(landlord)
                
                # Create demo tenant
                tenant = User(
                    email='tenant@example.com',
                    first_name='Jane',
                    last_name='Tenant',
                    role='tenant'
                )
                tenant.set_password('password123')
                db.session.add(tenant)
                
                # Create admin user
                admin = User(
                    email='admin@example.com',
                    first_name='Admin',
                    last_name='User',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                
                db.session.commit()
                print("✅ Demo users created")
            else:
                print("✅ Demo users already exist")
                
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    init_production_database()