import unittest
from app import create_app
from app.models import db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_register(self):
        response = self.client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'tenant'
        })
        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        # Create user first
        with self.app.app_context():
            user = User(email='test@example.com', first_name='Test', last_name='User')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        response = self.client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)