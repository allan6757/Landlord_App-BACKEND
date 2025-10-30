# ============================================================================
# PAYMENT MODEL - Rent Payment Management
# ============================================================================
# Defines Payment model for rent payment tracking and M-Pesa integration
#
# REQUIRED FIELDS:
# - amount: Payment amount
# - status: Payment status (pending/completed/failed)
# - due_date: Payment due date (stored as payment_date)
# - property_id: Associated property (foreign key)
# - tenant_id: Tenant making payment (foreign key)
#
# M-PESA FIELDS:
# - mpesa_checkout_id: M-Pesa STK Push request ID
# - phone_number: Phone number for M-Pesa payment
# - reference: Unique payment reference
#
# API RESPONSE FORMAT:
# {
#   "id": 1,
#   "amount": 1500.00,
#   "status": "completed",
#   "due_date": "2024-01-15T00:00:00",
#   "property": {...},
#   "tenant": {...}
# }
#
# M-PESA STK PUSH FLOW:
# 1. POST /api/payments with phone_number and amount
# 2. Backend initiates M-Pesa STK Push
# 3. User enters M-Pesa PIN on phone
# 4. M-Pesa sends callback to /api/payments/callback
# 5. Payment status updated to 'completed' or 'failed'
# ============================================================================

from .base import BaseModel, db
from sqlalchemy.dialects.postgresql import ENUM
import enum

class PaymentStatus(enum.Enum):
    """Payment status enumeration"""
    PENDING = 'pending'      # Awaiting payment
    COMPLETED = 'completed'  # Payment successful
    FAILED = 'failed'        # Payment failed
    CANCELLED = 'cancelled'  # Payment cancelled

class PaymentMethod(enum.Enum):
    """Payment method enumeration"""
    MPESA = 'mpesa'  # M-Pesa mobile money
    BANK = 'bank'    # Bank transfer
    CASH = 'cash'    # Cash payment
    CARD = 'card'    # Card payment

class Payment(BaseModel):
    """Payment model for rent payment tracking"""
    __tablename__ = 'payments'
    
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(ENUM(PaymentMethod), default=PaymentMethod.MPESA)
    status = db.Column(ENUM(PaymentStatus), default=PaymentStatus.PENDING)
    reference = db.Column(db.String(100), unique=True)
    mpesa_checkout_id = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    property = db.relationship('Property', backref='payments')
    tenant = db.relationship('User', backref='payments')
    
    def to_dict(self):
        """Serialize payment to dictionary for API responses
        Returns payment with property and tenant details
        """
        return {
            'id': self.id,
            'amount': float(self.amount) if self.amount else None,
            'due_date': self.payment_date.isoformat() if self.payment_date else None,  # Frontend expects 'due_date'
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'status': self.status.value if self.status else None,  # 'pending', 'completed', 'failed'
            'reference': self.reference,
            'phone_number': self.phone_number,
            'property_id': self.property_id,
            'tenant_id': self.tenant_id,
            'property': self.property.to_dict() if self.property else None,  # Full property details
            'tenant': self.tenant.to_dict() if self.tenant else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }