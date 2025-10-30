# ============================================================================
# PROPMANAGER PROPERTY MANAGEMENT SYSTEM - MAIN APPLICATION ENTRY POINT
# ============================================================================
# This file starts the Flask REST API server with Socket.IO support
#
# SETUP COMMANDS:
# 1. Install dependencies: pip install -r requirements.txt
# 2. Set environment variables in .env file (see .env.example)
# 3. Initialize database: python init_db.py
# 4. Run development server: python run.py
# 5. Run production server: gunicorn --worker-class eventlet -w 1 run:app
#
# API ENDPOINTS:
# - POST /api/auth/register - Register new user (landlord/tenant)
# - POST /api/auth/login - Login and get JWT token
# - GET /api/auth/profile - Get current user profile
# - GET /api/properties - List properties (filtered by role)
# - POST /api/properties - Create property (landlord only)
# - GET /api/payments - List payments (filtered by role)
# - POST /api/payments - Create payment with M-Pesa STK Push
# - GET /api/conversations - List chat conversations
# - POST /api/conversations - Create new conversation
# - GET /api/conversations/<id>/messages - Get messages
# - POST /api/conversations/<id>/messages - Send message
#
# AUTHENTICATION:
# - Include JWT token in headers: Authorization: Bearer <token>
# - Token expires after 24 hours (configurable in config.py)
#
# DATABASE:
# - Development: SQLite (landlord_app.db)
# - Production: PostgreSQL (set DATABASE_URL environment variable)
# ============================================================================

from app import create_app, db, socketio
from flask_migrate import Migrate
import os

# Create Flask application instance with configuration
app = create_app()

# Initialize Flask-Migrate for database migrations
# Commands: flask db init, flask db migrate, flask db upgrade
migrate = Migrate(app, db)

# Create database tables on startup
with app.app_context():
    try:
        # Import all models to register them with SQLAlchemy
        from app.models import User, Property, Payment, Conversation, Message
        # Create all tables defined in models
        db.create_all()
        app.logger.info("Database tables created successfully")
    except Exception as e:
        app.logger.error(f"Database initialization error: {e}")

if __name__ == '__main__':
    # Get port from environment variable or use default 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Start server with Socket.IO support for real-time chat
    # Use socketio.run() instead of app.run() for WebSocket functionality
    socketio.run(
        app,
        host='0.0.0.0',  # Listen on all network interfaces
        port=port,
        debug=app.config.get('DEBUG', False)
    )