import pytest
from app import create_app
from app.models import db, User, Property

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Create test user and get token
    user = User(email='landlord@test.com', first_name='Test', last_name='Landlord', role='landlord')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/login', json={
        'email': 'landlord@test.com',
        'password': 'password123'
    })
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}

def test_create_property(client, auth_headers):
    response = client.post('/api/properties/', json={
        'title': 'Test Property',
        'address': '123 Test St',
        'city': 'Test City',
        'state': 'TS',
        'zip_code': '12345',
        'property_type': 'apartment',
        'monthly_rent': 1500.00
    }, headers=auth_headers)

    assert response.status_code == 201
    assert response.json['property']['title'] == 'Test Property'

def test_get_properties(client, auth_headers):
    response = client.get('/api/properties/', headers=auth_headers)
    assert response.status_code == 200
    assert 'properties' in response.json

def test_unauthorized_access(client):
    response = client.get('/api/properties/')
    assert response.status_code == 401