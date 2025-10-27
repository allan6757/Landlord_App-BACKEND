# Email Service using SendGrid
# Handles all email notifications including verification emails

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    """
    Service class for sending emails via SendGrid
    """
    
    def __init__(self):
        # Get SendGrid API key from environment variables
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        self.from_email = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@rentalplatform.com')
        
    def send_email(self, to_email, subject, html_content):
        """
        Send an email using SendGrid
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_content: HTML content of the email
            
        Returns:
            Boolean indicating success or failure
        """
        # Check if SendGrid is configured
        if not self.api_key:
            print("Warning: SendGrid API key not configured")
            return False
        
        try:
            # Create email message
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            # Send email via SendGrid
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            # Check if email was sent successfully
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def send_verification_email(self, user_email, user_name, verification_token):
        """
        Send email verification link to new users
        
        Args:
            user_email: User's email address
            user_name: User's full name
            verification_token: Unique verification token
        """
        # Get frontend URL from environment
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        verification_link = f"{frontend_url}/verify-email?token={verification_token}"
        
        # Create HTML email content
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Welcome to Rental Platform, {user_name}!</h2>
                <p>Thank you for registering. Please verify your email address to activate your account.</p>
                <p>
                    <a href="{verification_link}" 
                       style="background-color: #4CAF50; color: white; padding: 10px 20px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Verify Email Address
                    </a>
                </p>
                <p>Or copy and paste this link in your browser:</p>
                <p>{verification_link}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't create an account, please ignore this email.</p>
            </body>
        </html>
        """
        
        return self.send_email(
            to_email=user_email,
            subject="Verify Your Email - Rental Platform",
            html_content=html_content
        )
    
    def send_password_reset_email(self, user_email, user_name, reset_token):
        """
        Send password reset link to users
        
        Args:
            user_email: User's email address
            user_name: User's full name
            reset_token: Unique password reset token
        """
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        reset_link = f"{frontend_url}/reset-password?token={reset_token}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Password Reset Request</h2>
                <p>Hi {user_name},</p>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                <p>
                    <a href="{reset_link}" 
                       style="background-color: #2196F3; color: white; padding: 10px 20px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Reset Password
                    </a>
                </p>
                <p>Or copy and paste this link in your browser:</p>
                <p>{reset_link}</p>
                <p>This link will expire in 1 hour.</p>
                <p>If you didn't request a password reset, please ignore this email.</p>
            </body>
        </html>
        """
        
        return self.send_email(
            to_email=user_email,
            subject="Password Reset - Rental Platform",
            html_content=html_content
        )
    
    def send_payment_confirmation(self, user_email, user_name, payment_details):
        """
        Send payment confirmation email
        
        Args:
            user_email: User's email address
            user_name: User's full name
            payment_details: Dictionary with payment information
        """
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Payment Confirmation</h2>
                <p>Hi {user_name},</p>
                <p>Your payment has been received successfully.</p>
                <h3>Payment Details:</h3>
                <ul>
                    <li><strong>Amount:</strong> ${payment_details.get('amount', 0)}</li>
                    <li><strong>Property:</strong> {payment_details.get('property_name', 'N/A')}</li>
                    <li><strong>Date:</strong> {payment_details.get('date', 'N/A')}</li>
                    <li><strong>Transaction ID:</strong> {payment_details.get('transaction_id', 'N/A')}</li>
                </ul>
                <p>Thank you for your payment!</p>
            </body>
        </html>
        """
        
        return self.send_email(
            to_email=user_email,
            subject="Payment Confirmation - Rental Platform",
            html_content=html_content
        )

# Create a singleton instance
email_service = EmailService()
