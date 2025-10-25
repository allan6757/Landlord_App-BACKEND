from .base import BaseModel, db

class Property(BaseModel):
    __tablename__ = 'properties'
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255), nullable=False)
    rent_amount = db.Column(db.Numeric(10, 2), nullable=False)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    area = db.Column(db.Float)
    property_type = db.Column(db.String(50))  # apartment, house, etc.
    status = db.Column(db.String(20), default='available')  # available, rented
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    landlord = db.relationship('User', foreign_keys=[landlord_id], backref='owned_properties')
    tenant = db.relationship('User', foreign_keys=[tenant_id], backref='rented_properties')