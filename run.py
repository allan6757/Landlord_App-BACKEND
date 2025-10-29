from app import create_app
from app.models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

app = create_app()
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config.get('DEBUG', False)
    )