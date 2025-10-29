from .base import BaseModel, db
from sqlalchemy.dialects.postgresql import ENUM
import enum

class PropertyStatus(enum.Enum):
    AVAILABLE = 'available'
    OCCUPIED = 'occupied'
    MAINTENANCE = 'maintenance'
    UNAVAILABLE = 'unavailable'

class PropertyType(enum.Enum):
    APARTMENT = 'apartment'
    HOUSE = 'house'
    CONDO = 'condo'
    TOWNHOUSE = 'townhouse'

class Property(BaseModel):
    __tablename__ = 'properties'

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    property_type = db.Column(ENUM(PropertyType), nullable=False)
    status = db.Column(ENUM(PropertyStatus), default=PropertyStatus.AVAILABLE)

    monthly_rent = db.Column(db.Numeric(10, 2), nullable=False)
    security_deposit = db.Column(db.Numeric(10, 2), default=0)
    lease_start = db.Column(db.Date)
    lease_end = db.Column(db.Date)

    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Numeric(3, 1))
    square_feet = db.Column(db.Integer)
    amenities = db.Column(db.Text)
    images = db.Column(db.JSON)  # Store Cloudinary URLs

    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    landlord = db.relationship('User', foreign_keys=[landlord_id], backref='owned_properties')
    tenant = db.relationship('User', foreign_keys=[tenant_id], backref='tenant_properties')
    conversations = db.relationship('Conversation', back_populates='property')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'property_type': self.property_type.value if self.property_type else None,
            'status': self.status.value if self.status else None,
            'monthly_rent': float(self.monthly_rent) if self.monthly_rent else None,
            'security_deposit': float(self.security_deposit) if self.security_deposit else None,
            'bedrooms': self.bedrooms,
            'bathrooms': float(self.bathrooms) if self.bathrooms else None,
            'square_feet': self.square_feet,
            'amenities': self.amenities,
            'images': self.images or [],
            'landlord_id': self.landlord_id,
            'tenant_id': self.tenant_id,
            'landlord': self.landlord.to_dict() if self.landlord else None,
            'tenant': self.tenant.to_dict() if self.tenant else None,
            'lease_start': self.lease_start.isoformat() if self.lease_start else None,
            'lease_end': self.lease_end.isoformat() if self.lease_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }