from flask_restful import Resource
from flask import jsonify
from app import db
import os

class HealthCheck(Resource):
    def get(self):
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'
        
        return {
            'status': 'healthy',
            'message': 'Rental Platform API is running',
            'database': db_status,
            'environment': os.environ.get('FLASK_ENV', 'development')
        }, 200