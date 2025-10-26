#!/usr/bin/env python3
"""
Database setup script for the Rental Platform
Creates database, runs migrations, and sets up initial data
"""

import os
import sys
from app import create_app, db
from app.models import User, UserProfile, UserRole
from flask_migrate import upgrade

def setup_database():
    """Initialize database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        print("Setting up sample users...")
        
        # Create sample landlord
        if not User.query.filter_by(email='landlord@example.com').first():
            landlord = User(
                email='landlord@example.com',
                first_name='John',
                last_name='Landlord',
                is_verified=True
            )
            landlord.set_password('password123')
            db.session.add(landlord)
            db.session.commit()
            
            landlord_profile = UserProfile(
                user_id=landlord.id,
                role=UserRole.LANDLORD,
                phone='+1234567890',
                address='123 Owner Street'
            )
            db.session.add(landlord_profile)
        
        # Create sample tenant
        if not User.query.filter_by(email='tenant@example.com').first():
            tenant = User(
                email='tenant@example.com',
                first_name='Jane',
                last_name='Tenant',
                is_verified=True
            )
            tenant.set_password('password123')
            db.session.add(tenant)
            db.session.commit()
            
            tenant_profile = UserProfile(
                user_id=tenant.id,
                role=UserRole.TENANT,
                phone='+0987654321',
                address='456 Renter Avenue'
            )
            db.session.add(tenant_profile)
        
        db.session.commit()
        print("Database setup completed successfully!")
        print("\nSample accounts created:")
        print("Landlord: landlord@example.com / password123")
        print("Tenant: tenant@example.com / password123")

if __name__ == '__main__':
    setup_database()