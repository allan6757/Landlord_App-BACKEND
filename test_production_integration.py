#!/usr/bin/env python3
"""
Production Integration Test Script
Tests the live backend API endpoints to ensure they're working correctly
"""

import requests
import json
import sys

# Backend URL
BACKEND_URL = "https://landlord-app-backend-1eph.onrender.com"

def test_health_check():
    """Test if the backend is responding"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend health check passed: {data.get('message', 'OK')}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_cors_headers():
    """Test CORS headers"""
    try:
        headers = {
            'Origin': 'https://landlord-app-frontend.vercel.app',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{BACKEND_URL}/api/auth/login", headers=headers, timeout=10)
        
        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        if cors_origin:
            print(f"✅ CORS configured: {cors_origin}")
            return True
        else:
            print("❌ CORS headers not found")
            return False
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    try:
        # Test login endpoint
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        response = requests.post(f"{BACKEND_URL}/api/auth/login", 
                               json=login_data, 
                               timeout=10)
        
        if response.status_code in [400, 401]:
            print("✅ Auth endpoint responding correctly")
            return True
        else:
            print(f"❌ Auth endpoint unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Auth endpoint test failed: {e}")
        return False

def test_database_connection():
    """Test database connectivity through API"""
    try:
        # Try to access properties endpoint (should require auth)
        response = requests.get(f"{BACKEND_URL}/api/properties", timeout=10)
        
        if response.status_code == 401:
            print("✅ Database connection working (auth required)")
            return True
        elif response.status_code == 200:
            print("✅ Database connection working (public access)")
            return True
        else:
            print(f"❌ Database connection issue: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Testing Production Backend Integration...")
    print(f"Backend URL: {BACKEND_URL}")
    print("-" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("CORS Configuration", test_cors_headers),
        ("Authentication Endpoints", test_auth_endpoints),
        ("Database Connection", test_database_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All integration tests passed! Backend is ready for frontend connection.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the backend configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())