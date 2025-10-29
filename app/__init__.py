from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from app.config import Config, ProductionConfig
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api()
cors = CORS()
socketio = SocketIO(cors_allowed_origins="*", async_mode='eventlet')

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
    cors.init_app(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}}, supports_credentials=True)
    socketio.init_app(app, cors_allowed_origins=app.config['CORS_ORIGINS'])
    
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
        from app.resources.auth import Register, Login, Profile
        from app.resources.users import UserList, UserDetail, UserProfileImage
        from app.resources.properties import PropertyList, PropertyDetail, PropertyImages
        from app.resources.payments import PaymentList, PaymentDetail, PaymentCallback
        from app.resources.chat import ConversationList, ConversationDetail, MessageList
        from app.resources.dashboard import LandlordDashboard, TenantDashboard
        
        # Authentication routes
        api.add_resource(Register, '/api/auth/register')
        api.add_resource(Login, '/api/auth/login')
        api.add_resource(Profile, '/api/auth/profile')
        
        # User routes
        api.add_resource(UserList, '/api/users')
        api.add_resource(UserDetail, '/api/users/<int:user_id>')
        api.add_resource(UserProfileImage, '/api/users/profile-image')
        
        # Property routes
        api.add_resource(PropertyList, '/api/properties')
        api.add_resource(PropertyDetail, '/api/properties/<int:property_id>')
        api.add_resource(PropertyImages, '/api/properties/<int:property_id>/images')
        
        # Payment routes
        api.add_resource(PaymentList, '/api/payments')
        api.add_resource(PaymentDetail, '/api/payments/<int:payment_id>')
        api.add_resource(PaymentCallback, '/api/payments/callback')
        
        # Chat routes
        api.add_resource(ConversationList, '/api/conversations')
        api.add_resource(ConversationDetail, '/api/conversations/<int:conversation_id>')
        api.add_resource(MessageList, '/api/conversations/<int:conversation_id>/messages')
        
        # Dashboard routes
        api.add_resource(LandlordDashboard, '/api/dashboard/landlord')
        api.add_resource(TenantDashboard, '/api/dashboard/tenant')
        
    except ImportError as e:
        app.logger.error(f"Failed to import resources: {e}")
    
    api.init_app(app)
    
    # Register Socket.IO handlers
    try:
        import app.sockets
        app.logger.info("Socket.IO handlers registered")
    except Exception as e:
        app.logger.warning(f"Socket.IO handler registration skipped: {e}")
    
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
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    return app