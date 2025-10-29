import requests
import base64
from datetime import datetime
from flask import current_app

class MPesaService:
    def __init__(self):
        self.consumer_key = current_app.config['MPESA_CONSUMER_KEY']
        self.consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']
        self.business_shortcode = current_app.config['MPESA_BUSINESS_SHORTCODE']
        self.passkey = current_app.config['MPESA_PASSKEY']
        self.base_url = "https://sandbox.safaricom.co.ke"
    
    def get_access_token(self):
        try:
            url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
            credentials = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
            
            headers = {
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()['access_token']
        except Exception as e:
            current_app.logger.error(f"MPesa token error: {str(e)}")
        return None
    
    def initiate_payment(self, phone_number, amount, account_reference):
        token = self.get_access_token()
        if not token:
            return {'error': 'Failed to get access token'}
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.business_shortcode}{self.passkey}{timestamp}".encode()).decode()
        
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": f"{current_app.config['FRONTEND_URL']}/api/payments/callback",
            "AccountReference": account_reference,
            "TransactionDesc": "Rent Payment"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            return {'error': str(e)}