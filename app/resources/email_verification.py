# Email Verification Resources
# Handles 2-step email verification process (Optional but Recommended for Capstone)

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.verification import VerificationToken
from app.utils.email_service import email_service
from flasgger import swag_from

class SendVerificationEmail(Resource):
    """
    Send or resend email verification link
    """
    
    @jwt_required()
    def post(self):
        """
        Send verification email to current user
        ---
        tags:
          - Authentication
        security:
          - Bearer: []
        responses:
          200:
            description: Verification email sent successfully
          400:
            description: User already verified
          500:
            description: Failed to send email
        """
        try:
            # Get current user
            user_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            
            # Check if already verified
            if user.is_verified:
                return {'message': 'Email already verified'}, 400
            
            # Create verification token
            token = VerificationToken.create_email_verification_token(user.id)
            db.session.add(token)
            db.session.commit()
            
            # Send verification email
            full_name = f"{user.first_name} {user.last_name}"
            success = email_service.send_verification_email(
                user_email=user.email,
                user_name=full_name,
                verification_token=token.token
            )
            
            if success:
                return {
                    'message': 'Verification email sent successfully. Please check your inbox.'
                }, 200
            else:
                return {
                    'error': 'Failed to send verification email. Please try again later.'
                }, 500
                
        except Exception as e:
            db.session.rollback()
            return {'error': f'An error occurred: {str(e)}'}, 500

class VerifyEmail(Resource):
    """
    Verify email using token from email link
    """
    
    def post(self):
        """
        Verify user email with token
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - token
              properties:
                token:
                  type: string
                  description: Verification token from email
        responses:
          200:
            description: Email verified successfully
          400:
            description: Invalid or expired token
          404:
            description: Token not found
        """
        data = request.get_json()
        token_string = data.get('token')
        
        if not token_string:
            return {'error': 'Verification token is required'}, 400
        
        try:
            # Find token in database
            token = VerificationToken.query.filter_by(
                token=token_string,
                token_type='email_verification'
            ).first()
            
            if not token:
                return {'error': 'Invalid verification token'}, 404
            
            # Check if token is valid
            if not token.is_valid():
                return {'error': 'Token has expired or already been used'}, 400
            
            # Mark user as verified
            user = User.query.get(token.user_id)
            user.is_verified = True
            
            # Mark token as used
            token.mark_as_used()
            
            db.session.commit()
            
            return {
                'message': 'Email verified successfully! You can now access all features.'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Verification failed: {str(e)}'}, 500

class RequestPasswordReset(Resource):
    """
    Request password reset email
    """
    
    def post(self):
        """
        Send password reset email
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - email
              properties:
                email:
                  type: string
                  description: User's email address
        responses:
          200:
            description: Password reset email sent
          404:
            description: User not found
        """
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return {'error': 'Email is required'}, 400
        
        try:
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            # Always return success to prevent email enumeration
            if not user:
                return {
                    'message': 'If an account exists with this email, a password reset link has been sent.'
                }, 200
            
            # Create password reset token
            token = VerificationToken.create_password_reset_token(user.id)
            db.session.add(token)
            db.session.commit()
            
            # Send password reset email
            full_name = f"{user.first_name} {user.last_name}"
            email_service.send_password_reset_email(
                user_email=user.email,
                user_name=full_name,
                reset_token=token.token
            )
            
            return {
                'message': 'If an account exists with this email, a password reset link has been sent.'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to process request'}, 500

class ResetPassword(Resource):
    """
    Reset password using token from email
    """
    
    def post(self):
        """
        Reset password with token
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - token
                - new_password
              properties:
                token:
                  type: string
                  description: Password reset token from email
                new_password:
                  type: string
                  description: New password (min 8 characters)
        responses:
          200:
            description: Password reset successfully
          400:
            description: Invalid or expired token
        """
        data = request.get_json()
        token_string = data.get('token')
        new_password = data.get('new_password')
        
        # Validate input
        if not token_string or not new_password:
            return {'error': 'Token and new password are required'}, 400
        
        if len(new_password) < 8:
            return {'error': 'Password must be at least 8 characters long'}, 400
        
        try:
            # Find token
            token = VerificationToken.query.filter_by(
                token=token_string,
                token_type='password_reset'
            ).first()
            
            if not token:
                return {'error': 'Invalid reset token'}, 404
            
            # Check if token is valid
            if not token.is_valid():
                return {'error': 'Token has expired or already been used'}, 400
            
            # Update user password
            user = User.query.get(token.user_id)
            user.set_password(new_password)
            
            # Mark token as used
            token.mark_as_used()
            
            db.session.commit()
            
            return {
                'message': 'Password reset successfully! You can now login with your new password.'
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Password reset failed: {str(e)}'}, 500
