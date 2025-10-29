#!/usr/bin/env python3
"""
Reset production database
Drops and recreates all tables with demo data
"""

import os
from app import create_app, db
from app.config import ProductionConfig

def reset_production_database():
    """Reset production database completely"""
    app = create_app(ProductionConfig)
    
    with app.app_context():
        try:
            # Import all models
            from app.models import User, Property, Payment, Conversation, Message
            
            print("🔄 Dropping all tables...")
            db.drop_all()
            
            print("🔄 Creating all tables...")
            db.create_all()
            
            print("🔄 Creating demo users...")
            
            # Create demo users
            users = [
                {
                    'email': 'landlord@example.com',
                    'password': 'password123',
                    'first_name': 'John',
                    'last_name': 'Landlord',
                    'role': 'landlord'
                },
                {
                    'email': 'tenant@example.com',
                    'password': 'password123',
                    'first_name': 'Jane',
                    'last_name': 'Tenant',
                    'role': 'tenant'
                },
                {
                    'email': 'admin@example.com',
                    'password': 'admin123',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'role': 'admin'
                }
            ]
            
            for user_data in users:
                user = User(
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data['role']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
            
            db.session.commit()
            print("✅ Database reset complete!")
            
        except Exception as e:
            print(f"❌ Database reset failed: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    reset_production_database()