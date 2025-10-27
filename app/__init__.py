from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config

# Initialize extensions
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
    CORS(app, origins=['https://landlord-app-frontend.vercel.app'], supports_credentials=True)
    
    # Initialize Swagger for API documentation (Required for Capstone)
    from app.swagger_config import swagger_config, swagger_template
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Register resources
    from app.resources.auth import Register, Login, Profile
    from app.resources.email_verification import (
        SendVerificationEmail, VerifyEmail, 
        RequestPasswordReset, ResetPassword
    )
    from app.resources.images import UploadPropertyImage, UploadProfileImage
    from app.resources.users import UserList, UserDetail
    from app.resources.properties import PropertyList, PropertyDetail
    from app.resources.payments import PaymentList, PaymentDetail
    from app.resources.chat import ConversationList, ConversationDetail, MessageList
    
    # Authentication routes
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Profile, '/api/auth/profile')
    
    # Email verification routes (2-step authentication)
    api.add_resource(SendVerificationEmail, '/api/auth/send-verification')
    api.add_resource(VerifyEmail, '/api/auth/verify-email')
    api.add_resource(RequestPasswordReset, '/api/auth/request-password-reset')
    api.add_resource(ResetPassword, '/api/auth/reset-password')
    
    # Image upload routes (Cloudinary)
    api.add_resource(UploadPropertyImage, '/api/properties/<int:property_id>/upload-image')
    api.add_resource(UploadProfileImage, '/api/users/upload-profile-image')
    
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
    
    # Manual CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'https://landlord-app-frontend.vercel.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Handle preflight OPTIONS requests
    @app.route('/api/<path:path>', methods=['OPTIONS'])
    def handle_options(path):
        return '', 200
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Rental Platform API is running'}, 200
    
    # Global error handlers for better error messages
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error. Please try again later'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request. Please check your input'}), 400
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired. Please login again'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token. Please login again'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authorization token is missing'}), 401
    
    return app