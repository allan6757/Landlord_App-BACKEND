from flask import current_app

def send_email(to_email, subject, html_content):
    """Send email with error handling"""
    try:
        if not current_app.config.get('SENDGRID_API_KEY'):
            current_app.logger.warning("SendGrid not configured, skipping email")
            return False
            
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        message = Mail(
            from_email=current_app.config['SENDGRID_FROM_EMAIL'],
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        sg = SendGridAPIClient(api_key=current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        current_app.logger.error(f"Email sending failed: {str(e)}")
        return False

def send_welcome_email(user):
    """Send welcome email to new user"""
    if not current_app.config.get('SENDGRID_API_KEY'):
        return False
        
    subject = "Welcome to Rental Platform"
    html_content = f"""
    <h2>Welcome {user.first_name}!</h2>
    <p>Your account has been created successfully.</p>
    <p>Role: {user.role.title()}</p>
    <p>You can now log in to your dashboard.</p>
    """
    return send_email(user.email, subject, html_content)

def send_payment_confirmation(payment):
    """Send payment confirmation email"""
    if not current_app.config.get('SENDGRID_API_KEY'):
        return False
        
    subject = "Payment Confirmation"
    html_content = f"""
    <h2>Payment Confirmed</h2>
    <p>Amount: ${payment.amount}</p>
    <p>Property: {payment.property.title}</p>
    <p>Date: {payment.payment_date.strftime('%Y-%m-%d')}</p>
    <p>Reference: {payment.reference}</p>
    """
    return send_email(payment.tenant.email, subject, html_content)