from .base import BaseModel, db
from sqlalchemy.dialects.postgresql import ENUM
import enum
from datetime import datetime

class PaymentStatus(enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class PaymentMethod(enum.Enum):
    MPESA = 'mpesa'
    BANK_TRANSFER = 'bank_transfer'
    CASH = 'cash'
    CARD = 'card'

class Payment(BaseModel):
    __tablename__ = 'payments'
    
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_method = db.Column(ENUM(PaymentMethod), nullable=False)
    status = db.Column(ENUM(PaymentStatus), default=PaymentStatus.PENDING)
    reference = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    
    property = db.relationship('Property', backref='payments')
    tenant_user = db.relationship('UserProfile', foreign_keys=[tenant_id], backref='sent_payments')
    landlord_user = db.relationship('UserProfile', foreign_keys=[landlord_id], backref='received_payments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount) if self.amount else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'status': self.status.value if self.status else None,
            'reference': self.reference,
            'description': self.description,
            'property_id': self.property_id,
            'tenant_id': self.tenant_id,
            'landlord_id': self.landlord_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }