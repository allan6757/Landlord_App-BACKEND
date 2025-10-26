from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    # Register resources
    from app.resources.auth import Register, Login, Profile
    from app.resources.users import UserList, UserDetail
    from app.resources.properties import PropertyList, PropertyDetail
    from app.resources.payments import PaymentList, PaymentDetail
    from app.resources.chat import ConversationList, ConversationDetail, MessageList
    
    # Authentication routes
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Profile, '/api/auth/profile')
    
    # User routes
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserDetail, '/api/users/<int:user_id>')
    
    # Property routes
    api.add_resource(PropertyList, '/api/properties')
    api.add_resource(PropertyDetail, '/api/properties/<int:property_id>')
    
    # Payment routes
    api.add_resource(PaymentList, '/api/payments')
    api.add_resource(PaymentDetail, '/api/payments/<int:payment_id>')
    
    # Chat routes
    api.add_resource(ConversationList, '/api/conversations')
    api.add_resource(ConversationDetail, '/api/conversations/<int:conversation_id>')
    api.add_resource(MessageList, '/api/conversations/<int:conversation_id>/messages')
    
    api.init_app(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Rental Platform API is running'}, 200
    
    return app