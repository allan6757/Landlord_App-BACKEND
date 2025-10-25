import pytest
from app import create_app, db
from app.models.user import User
from app.models.chat import Conversation, Message

@pytest.fixture
def app():
    from app.config import TestingConfig
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_users(app):
    with app.app_context():
        # Create two users
        user1 = User(email='user1@test.com', first_name='John', last_name='Doe', role='landlord')
        user1.set_password('password123')
        
        user2 = User(email='user2@test.com', first_name='Jane', last_name='Smith', role='tenant')
        user2.set_password('password123')
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        return {'user1': user1, 'user2': user2}

def test_create_conversation(client, test_users):
    # Login as user1
    response = client.post('/api/auth/login', json={
        'email': 'user1@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    response = client.post('/api/conversations', json={
        'participant_id': test_users['user2'].id,
        'title': 'Test Conversation'
    }, headers=headers)
    
    assert response.status_code == 201
    assert response.json['conversation']['title'] == 'Test Conversation'

def test_send_message(client, test_users):
    # Login as user1
    response = client.post('/api/auth/login', json={
        'email': 'user1@test.com',
        'password': 'password123'
    })
    token = response.json['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create conversation
    conv_response = client.post('/api/conversations', json={
        'participant_id': test_users['user2'].id,
        'title': 'Test Conversation'
    }, headers=headers)
    
    conversation_id = conv_response.json['conversation']['id']
    
    # Send message
    response = client.post(f'/api/conversations/{conversation_id}/messages', json={
        'content': 'Hello, this is a test message!'
    }, headers=headers)
    
    assert response.status_code == 201
    assert response.json['message']['content'] == 'Hello, this is a test message!'