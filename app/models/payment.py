from .base import BaseModel, db
from sqlalchemy.dialects.postgresql import ENUM
import enum

class PaymentStatus(enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class PaymentMethod(enum.Enum):
    MPESA = 'mpesa'
    BANK = 'bank'
    CASH = 'cash'
    CARD = 'card'

class Payment(BaseModel):
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
        return {
            'id': self.id,
            'amount': float(self.amount) if self.amount else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'status': self.status.value if self.status else None,
            'reference': self.reference,
            'phone_number': self.phone_number,
            'property_id': self.property_id,
            'tenant_id': self.tenant_id,
            'property': self.property.to_dict() if self.property else None,
            'tenant': self.tenant.to_dict() if self.tenant else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }