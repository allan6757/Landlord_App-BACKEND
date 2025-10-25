import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://rental_user:rental_password@localhost:5432/rental_platform'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    
    # Security Configuration
    BCRYPT_LOG_ROUNDS = 12
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # MPesa Configuration (for payments)
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', '')
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', '')
    MPESA_BUSINESS_SHORTCODE = os.environ.get('MPESA_BUSINESS_SHORTCODE', '174379')
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', '')
    
    # Email Configuration (for notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)