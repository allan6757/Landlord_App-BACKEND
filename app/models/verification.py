# Email Verification Token Model
# Stores tokens for email verification and password reset

from app import db
from app.models.base import BaseModel
from datetime import datetime, timedelta
import secrets

class VerificationToken(BaseModel):
    """
    Model for storing email verification and password reset tokens
    """
    __tablename__ = 'verification_tokens'
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Token string (unique and secure)
    token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Token type: 'email_verification' or 'password_reset'
    token_type = db.Column(db.String(20), nullable=False)
    
    # Expiration time
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Whether token has been used
    is_used = db.Column(db.Boolean, default=False)
    
    # Relationship to user
    user = db.relationship('User', backref='verification_tokens')
    
    @staticmethod
    def generate_token():
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def create_email_verification_token(cls, user_id):
        """
        Create a new email verification token
        
        Args:
            user_id: ID of the user
            
        Returns:
            VerificationToken instance
        """
        token = cls(
            user_id=user_id,
            token=cls.generate_token(),
            token_type='email_verification',
            expires_at=datetime.utcnow() + timedelta(hours=24)  # Valid for 24 hours
        )
        return token
    
    @classmethod
    def create_password_reset_token(cls, user_id):
        """
        Create a new password reset token
        
        Args:
            user_id: ID of the user
            
        Returns:
            VerificationToken instance
        """
        token = cls(
            user_id=user_id,
            token=cls.generate_token(),
            token_type='password_reset',
            expires_at=datetime.utcnow() + timedelta(hours=1)  # Valid for 1 hour
        )
        return token
    
    def is_valid(self):
        """
        Check if token is still valid
        
        Returns:
            Boolean indicating if token is valid
        """
        # Token is valid if not used and not expired
        return not self.is_used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self):
        """Mark token as used"""
        self.is_used = True
    
    def to_dict(self):
        """Convert token to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token_type': self.token_type,
            'expires_at': self.expires_at.isoformat(),
            'is_used': self.is_used,
            'created_at': self.created_at.isoformat()
        }
