from app import db, bcrypt
from app.models.base import BaseModel
from sqlalchemy.dialects.postgresql import ENUM
import enum

class UserRole(enum.Enum):
    LANDLORD = 'landlord'
    TENANT = 'tenant'
    ADMIN = 'admin'

class UserProfile(BaseModel):
    __tablename__ = 'user_profiles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(ENUM(UserRole), nullable=False, default=UserRole.TENANT)
    date_of_birth = db.Column(db.Date)
    emergency_contact = db.Column(db.String(100))

    user = db.relationship('User', back_populates='profile', uselist=False)
    owned_properties = db.relationship('Property', back_populates='landlord', foreign_keys='Property.landlord_id')
    tenant_properties = db.relationship('Property', back_populates='tenant', foreign_keys='Property.tenant_id')
    sent_payments = db.relationship('Payment', back_populates='tenant_user', foreign_keys='Payment.tenant_id')
    received_payments = db.relationship('Payment', back_populates='landlord_user', foreign_keys='Payment.landlord_id')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'phone': self.phone,
            'address': self.address,
            'role': self.role.value,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'emergency_contact': self.emergency_contact,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(BaseModel):
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    conversations_initiated = db.relationship('Conversation', back_populates='initiator', foreign_keys='Conversation.initiator_id')
    conversations_received = db.relationship('Conversation', back_populates='participant', foreign_keys='Conversation.participant_id')
    messages = db.relationship('Message', back_populates='sender')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_last_login(self):
        from datetime import datetime
        self.last_login = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile': self.profile.to_dict() if self.profile else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }