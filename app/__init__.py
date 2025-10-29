from flask import Flask, jsonify, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config, ProductionConfig
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api()
cors = CORS()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Determine config class based on environment
    if config_class is None:
        if os.environ.get('FLASK_ENV') == 'production':
            config_class = ProductionConfig
        else:
            config_class = Config
    
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, 
                  origins=app.config['CORS_ORIGINS'], 
                  supports_credentials=True,
                  allow_headers=['Content-Type', 'Authorization', 'Accept'],
                  methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Import models to ensure they're registered
    try:
        from app.models import User, Property, Payment, Conversation, Message
        app.logger.info("Models imported successfully")
    except Exception as e:
        app.logger.error(f"Model import failed: {e}")
    
    # Initialize Cloudinary only if credentials are provided
    if app.config.get('CLOUDINARY_CLOUD_NAME'):
        try:
            from app.utils.cloudinary import init_cloudinary
            with app.app_context():
                init_cloudinary()
        except Exception as e:
            app.logger.warning(f"Cloudinary initialization failed: {e}")
    
    # Register resources with error handling
    try:
        # Simple authentication routes that work
        from app.simple_routes import SimpleRegister, SimpleLogin
        api.add_resource(SimpleRegister, '/api/auth/register')
        api.add_resource(SimpleLogin, '/api/auth/login')
        app.logger.info("Auth routes registered")
        
    except Exception as e:
        app.logger.error(f"Failed to register auth routes: {e}")
    
    try:
        # User routes
        from app.resources.users import UserList, UserDetail, UserProfileImage
        api.add_resource(UserList, '/api/users')
        api.add_resource(UserDetail, '/api/users/<int:user_id>')
        api.add_resource(UserProfileImage, '/api/users/profile-image')
        app.logger.info("User routes registered")
        
    except Exception as e:
        app.logger.error(f"Failed to register user routes: {e}")
    
    try:
        # Property routes
        from app.resources.properties import PropertyList, PropertyDetail, PropertyImages
        api.add_resource(PropertyList, '/api/properties')
        api.add_resource(PropertyDetail, '/api/properties/<int:property_id>')
        api.add_resource(PropertyImages, '/api/properties/<int:property_id>/images')
        app.logger.info("Property routes registered")
        
    except Exception as e:
        app.logger.error(f"Failed to register property routes: {e}")
    
    try:
        # Payment routes
        from app.resources.payments import PaymentList, PaymentDetail, PaymentCallback
        api.add_resource(PaymentList, '/api/payments')
        api.add_resource(PaymentDetail, '/api/payments/<int:payment_id>')
        api.add_resource(PaymentCallback, '/api/payments/callback')
        app.logger.info("Payment routes registered")
        
    except Exception as e:
        app.logger.error(f"Failed to register payment routes: {e}")
    
    try:
        # Chat routes
        from app.resources.chat import ConversationList, ConversationDetail, MessageList
        api.add_resource(ConversationList, '/api/conversations')
        api.add_resource(ConversationDetail, '/api/conversations/<int:conversation_id>')
        api.add_resource(MessageList, '/api/conversations/<int:conversation_id>/messages')
        app.logger.info("Chat routes registered")
        
    except Exception as e:
        app.logger.error(f"Failed to register chat routes: {e}")
    
    try:
        # Dashboard routes
        from app.resources.dashboard import LandlordDashboard, TenantDashboard
        api.add_resource(LandlordDashboard, '/api/dashboard/landlord')
        api.add_resource(TenantDashboard, '/api/dashboard/tenant')
        app.logger.info("Dashboard routes registered")
        
    except Exception as e:
        app.logger.error(f"Failed to register dashboard routes: {e}")
    
    api.init_app(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return jsonify({
            'status': 'healthy',
            'message': 'Rental Platform API is running',
            'database': db_status,
            'environment': os.environ.get('FLASK_ENV', 'development')
        }), 200
    
    # Handle preflight OPTIONS requests
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
            response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
            return response
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    return app