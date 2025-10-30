# ============================================================================
# M-PESA INTEGRATION - Mobile Money Payment Processing
# ============================================================================
# M-Pesa STK Push (Lipa Na M-Pesa Online) integration for rent payments
#
# SETUP:
# 1. Register for M-Pesa Daraja API at https://developer.safaricom.co.ke
# 2. Create app and get Consumer Key and Consumer Secret
# 3. Set environment variables in .env:
#    MPESA_CONSUMER_KEY=your_consumer_key
#    MPESA_CONSUMER_SECRET=your_consumer_secret
#    MPESA_BUSINESS_SHORTCODE=174379
#    MPESA_PASSKEY=your_passkey
#
# FLOW:
# 1. User initiates payment from frontend
# 2. Backend calls stk_push() with phone number and amount
# 3. M-Pesa sends STK Push prompt to user's phone
# 4. User enters M-Pesa PIN
# 5. M-Pesa processes payment
# 6. M-Pesa sends callback to /api/payments/callback
# 7. Backend updates payment status
#
# PHONE NUMBER FORMAT:
# - Must be Kenyan number: 254XXXXXXXXX (12 digits)
# - Example: 254712345678
#
# TESTING:
# - Use Safaricom sandbox for testing
# - Sandbox URL: https://sandbox.safaricom.co.ke
# - Production URL: https://api.safaricom.co.ke
# ============================================================================

import requests
import base64
from datetime import datetime
import json

class MpesaClient:
    """M-Pesa API client for STK Push payments"""
    def __init__(self):
        """Initialize M-Pesa client with credentials from environment variables"""
        self.consumer_key = 'your_consumer_key'  # Set in .env: MPESA_CONSUMER_KEY
        self.consumer_secret = 'your_consumer_secret'  # Set in .env: MPESA_CONSUMER_SECRET
        self.business_shortcode = '174379'  # Set in .env: MPESA_BUSINESS_SHORTCODE
        self.passkey = 'your_passkey'  # Set in .env: MPESA_PASSKEY
        self.callback_url = 'https://yourdomain.com/api/payments/callback'  # Your callback URL
    
    def get_access_token(self):
        """Get OAuth access token from M-Pesa API
        Token is required for all M-Pesa API requests
        """
        # Encode credentials in Base64
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_auth}'
        }
        
        # Request access token from M-Pesa
        response = requests.get(
            'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
            headers=headers
        )
        
        return response.json().get('access_token')
    
    def stk_push(self, phone_number, amount, account_reference):
        """Initiate M-Pesa STK Push payment
        Sends payment prompt to user's phone
        
        Args:
            phone_number: Kenyan phone number (254XXXXXXXXX)
            amount: Payment amount in KES
            account_reference: Unique payment reference
        
        Returns:
            dict: M-Pesa response with CheckoutRequestID
        """
        # Get OAuth access token
        access_token = self.get_access_token()
        
        # Generate timestamp for password
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Generate password: Base64(Shortcode + Passkey + Timestamp)
        password = base64.b64encode(
            f"{self.business_shortcode}{self.passkey}{timestamp}".encode()
        ).decode()
        
        # STK Push request payload
        payload = {
            "BusinessShortCode": self.business_shortcode,  # Your paybill/till number
            "Password": password,  # Base64 encoded password
            "Timestamp": timestamp,  # YYYYMMDDHHmmss format
            "TransactionType": "CustomerPayBillOnline",  # Payment type
            "Amount": amount,  # Amount in KES
            "PartyA": phone_number,  # Customer phone number
            "PartyB": self.business_shortcode,  # Your paybill/till number
            "PhoneNumber": phone_number,  # Phone to receive STK Push
            "CallBackURL": self.callback_url,  # Callback endpoint
            "AccountReference": account_reference,  # Payment reference
            "TransactionDesc": "Rent Payment"  # Payment description
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Send STK Push request to M-Pesa
        response = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            json=payload,
            headers=headers
        )
        
        # Returns: {"CheckoutRequestID": "...", "ResponseCode": "0", ...}
        return response.json()
