import unittest
from app import create_app
from app.models import db, User, Payment

class PaymentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_get_payments(self):
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, 401)  # Requires auth