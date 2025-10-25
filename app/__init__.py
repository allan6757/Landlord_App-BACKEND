from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.resources.auth import auth_bp
    from app.resources.users import users_bp
    from app.resources.properties import properties_bp
    from app.resources.payments import payments_bp
    from app.resources.chat import chat_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(chat_bp)
    
    return app