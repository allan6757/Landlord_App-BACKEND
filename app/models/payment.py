from .base import BaseModel, db

class Payment(BaseModel):
    __tablename__ = 'payments'
    
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50))  # mpesa, bank, cash
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    reference = db.Column(db.String(100), unique=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    property = db.relationship('Property', backref='payments')
    tenant = db.relationship('User', backref='payments')