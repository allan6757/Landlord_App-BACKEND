#!/usr/bin/env python3
"""
Local development runner
Ensures proper configuration for local development
"""

import os
import sys
from pathlib import Path

# Set environment for local development
os.environ['FLASK_ENV'] = 'development'
os.environ['DATABASE_URL'] = 'sqlite:///landlord_app.db'

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from app import create_app, db
    from app.config import DevelopmentConfig
    
    # Create app with development config
    app = create_app(DevelopmentConfig)
    
    # Initialize database
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")
    
    print("🚀 Starting local development server...")
    print("📍 Backend: http://localhost:5000")
    print("📍 Health: http://localhost:5000/health")
    print("📍 API Docs: http://localhost:5000/api/")
    print("\n🔑 Test Accounts:")
    print("   Landlord: landlord@example.com / password123")
    print("   Tenant: tenant@example.com / password123")
    print("   Admin: admin@example.com / admin123")
    print("\n⏹️ Press Ctrl+C to stop\n")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
    
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("💡 Run: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Startup error: {e}")
    sys.exit(1)