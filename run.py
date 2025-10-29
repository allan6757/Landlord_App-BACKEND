from app import create_app, db
from flask_migrate import Migrate
import os

# Create app with appropriate config
app = create_app()

# Initialize database migration
migrate = Migrate(app, db)

# Ensure app context is available
with app.app_context():
    try:
        # Import models to register them
        from app.models import User, Property, Payment, Conversation, Message
        db.create_all()
        app.logger.info("Database tables created successfully")
    except Exception as e:
        app.logger.error(f"Database initialization error: {e}")

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config.get('DEBUG', False)
    )