from .base import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ENUM
import enum

class UserRole(enum.Enum):
    LANDLORD = 'landlord'
    TENANT = 'tenant'
    ADMIN = 'admin'

class User(BaseModel):
    __tablename__ = 'users'
    
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(ENUM(UserRole), default=UserRole.TENANT)
    is_active = db.Column(db.Boolean, default=True)
    profile_image = db.Column(db.String(255))
    
    # Relationships
    conversations_initiated = db.relationship('Conversation', foreign_keys='Conversation.initiator_id', back_populates='initiator')
    conversations_received = db.relationship('Conversation', foreign_keys='Conversation.participant_id', back_populates='participant')
    messages = db.relationship('Message', back_populates='sender')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role.value if self.role else None,
            'is_active': self.is_active,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }