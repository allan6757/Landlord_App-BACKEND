# ============================================================================
# USER MODEL - Authentication and User Management
# ============================================================================
# Defines User and Profile models for JWT-based authentication
#
# USER FIELDS:
# - id: Primary key (auto-generated)
# - email: Unique email for login
# - password_hash: Bcrypt hashed password
# - first_name: User's first name
# - profile: One-to-one relationship with Profile (contains role)
#
# PROFILE FIELDS:
# - id: Primary key
# - role: User role (landlord/tenant)
# - user_id: Foreign key to users table
#
# API RESPONSE FORMAT:
# {
#   "id": 1,
#   "email": "user@example.com",
#   "first_name": "John",
#   "profile": {"id": 1, "role": "tenant"}
# }
#
# USAGE:
# user = User(email='user@example.com', first_name='John')
# user.set_password('password123')
# profile = Profile(role='tenant')
# user.profile = profile
# db.session.add(user)
# db.session.commit()
# ============================================================================

from .base import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class UserRole(enum.Enum):
    """User role enumeration for role-based access control"""
    LANDLORD = 'landlord'  # Can create properties, view payments
    TENANT = 'tenant'      # Can view assigned properties, make payments
    ADMIN = 'admin'        # Full system access

class Profile(BaseModel):
    """Profile model containing user role information"""
    __tablename__ = 'profiles'
    
    role = db.Column(db.String(20), default='tenant', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role
        }

class User(BaseModel):
    __tablename__ = 'users'
    
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    profile_image = db.Column(db.String(255))
    
    # Profile relationship
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    
    # Relationships
    conversations_initiated = db.relationship('Conversation', foreign_keys='Conversation.initiator_id', back_populates='initiator', lazy='dynamic')
    conversations_received = db.relationship('Conversation', foreign_keys='Conversation.participant_id', back_populates='participant', lazy='dynamic')
    messages = db.relationship('Message', back_populates='sender', lazy='dynamic')
    
    @property
    def role(self):
        return self.profile.role if self.profile else 'tenant'
    
    def set_password(self, password):
        """Hash and store password securely using bcrypt"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against stored hash for login"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Serialize user to dictionary for API responses
        Returns user with profile.role format expected by frontend
        """
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'profile': self.profile.to_dict() if self.profile else {'id': None, 'role': 'tenant'}
        }