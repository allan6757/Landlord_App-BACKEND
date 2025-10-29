#!/usr/bin/env python3
"""
Database setup script for Rental Platform
Creates tables and sample data
"""

from app import create_app, db
from app.models import User, Property, Payment, Conversation, Message
from datetime import datetime, date
import os

def create_sample_data():
    """Create sample users and data for testing"""
    
    # Check if data already exists
    if User.query.first():
        print("⚠️  Sample data already exists. Skipping creation.")
        return
    
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
    
    # Create sample property
    property1 = Property(
        title='Modern 2BR Apartment',
        description='Beautiful modern apartment in the city center',
        address='123 Main Street',
        city='Nairobi',
        state='Nairobi',
        zip_code='00100',
        property_type='apartment',
        status='available',
        monthly_rent=50000,
        security_deposit=100000,
        bedrooms=2,
        bathrooms=2.0,
        square_feet=1200,
        amenities='WiFi, Parking, Security, Pool',
        landlord_id=landlord.id
    )
    
    property2 = Property(
        title='Cozy 1BR House',
        description='Small house perfect for single tenant',
        address='456 Oak Avenue',
        city='Nairobi',
        state='Nairobi',
        zip_code='00200',
        property_type='house',
        status='occupied',
        monthly_rent=35000,
        security_deposit=70000,
        bedrooms=1,
        bathrooms=1.0,
        square_feet=800,
        amenities='Garden, Parking',
        landlord_id=landlord.id,
        tenant_id=tenant.id,
        lease_start=date(2024, 1, 1),
        lease_end=date(2024, 12, 31)
    )
    
    db.session.add_all([property1, property2])
    db.session.commit()
    
    # Create sample payment
    payment = Payment(
        amount=35000,
        payment_date=datetime.utcnow(),
        payment_method='mpesa',
        status='completed',
        reference='PAY-2024-001',
        phone_number='+254700000002',
        property_id=property2.id,
        tenant_id=tenant.id
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # Create sample conversation
    conversation = Conversation(
        title='Property Inquiry',
        initiator_id=tenant.id,
        participant_id=landlord.id,
        property_id=property2.id
    )
    
    db.session.add(conversation)
    db.session.commit()
    
    # Create sample message
    message = Message(
        content='Hello, I have a question about the rent payment.',
        conversation_id=conversation.id,
        sender_id=tenant.id
    )
    
    db.session.add(message)
    conversation.update_last_message(message.content)
    
    print("✅ Sample data created successfully!")
    print("\nSample Accounts:")
    print("Landlord: landlord@example.com / password123")
    print("Tenant: tenant@example.com / password123")
    print("Admin: admin@example.com / admin123")

def main():
    """Main setup function"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Setting up database...")
        
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created!")
            
            # Create sample data
            create_sample_data()
            
        except Exception as e:
            print(f"❌ Database setup error: {e}")
            return
        
        print("\n🚀 Database setup complete!")
        print("You can now run: python run.py")

if __name__ == '__main__':
    main()