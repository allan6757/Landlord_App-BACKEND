import requests
import base64
from datetime import datetime
import json

class MpesaClient:
    def __init__(self):
        self.consumer_key = 'your_consumer_key'
        self.consumer_secret = 'your_consumer_secret'
        self.business_shortcode = '174379'
        self.passkey = 'your_passkey'
        self.callback_url = 'https://yourdomain.com/api/payments/callback'
    
    def get_access_token(self):
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_auth}'
        }
        
        response = requests.get(
            'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
            headers=headers
        )
        
        return response.json().get('access_token')
    
    def stk_push(self, phone_number, amount, account_reference):
        access_token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f"{self.business_shortcode}{self.passkey}{timestamp}".encode()
        ).decode()
        
        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": "Rent Payment"
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            json=payload,
            headers=headers
        )
        
        return response.json()
