import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration - Support both SQLite (local) and PostgreSQL (production)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Handle PostgreSQL URLs for production
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
        # PostgreSQL connection options
        if 'postgresql' in database_url:
            SQLALCHEMY_ENGINE_OPTIONS = {
                'pool_pre_ping': True,
                'pool_recycle': 300,
                'connect_args': {'sslmode': 'require'} if 'localhost' not in database_url else {}
            }
        else:
            SQLALCHEMY_ENGINE_OPTIONS = {}
    else:
        # Default to SQLite for local development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///landlord_app.db'
        SQLALCHEMY_ENGINE_OPTIONS = {}
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    
    # Security Configuration
    BCRYPT_LOG_ROUNDS = 12
    
    # CORS Configuration
    cors_origins = os.environ.get('CORS_ORIGINS', '*')
    if cors_origins == '*':
        CORS_ORIGINS = ['*']
    else:
        CORS_ORIGINS = cors_origins.split(',')
    
    # Optional Services (can be empty for local development)
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', '')
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', '')
    MPESA_BUSINESS_SHORTCODE = os.environ.get('MPESA_BUSINESS_SHORTCODE', '174379')
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', '')
    
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
    SENDGRID_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@rentalplatform.com')
    
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')
    
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # Force SQLite for local development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///landlord_app.db'
    SQLALCHEMY_ENGINE_OPTIONS = {}

class ProductionConfig(Config):
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    
    # Production CORS settings - Allow all Vercel domains
    cors_origins = os.environ.get('CORS_ORIGINS', '*')
    if cors_origins == '*':
        CORS_ORIGINS = ['*']
    else:
        CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    SQLALCHEMY_ENGINE_OPTIONS = {}