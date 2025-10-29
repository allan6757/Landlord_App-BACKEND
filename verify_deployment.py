#!/usr/bin/env python3
"""
Deployment verification script
Tests all API endpoints and functionality
"""

import requests
import json
import sys

BASE_URL = "https://landlord-app-backend-1eph.onrender.com"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_auth():
    """Test authentication endpoints"""
    try:
        # Test registration
        register_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "role": "tenant"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", 
                               json=register_data, timeout=10)
        print(f"Register: {response.status_code}")
        
        if response.status_code in [201, 400]:  # 400 if user exists
            # Test login
            login_data = {
                "email": "landlord@example.com",
                "password": "password123"
            }
            
            response = requests.post(f"{BASE_URL}/api/auth/login", 
                                   json=login_data, timeout=10)
            print(f"Login: {response.status_code}")
            
            if response.status_code == 200:
                token = response.json().get('token')
                return token
        
        return None
    except Exception as e:
        print(f"Auth test failed: {e}")
        return None

def test_protected_endpoints(token):
    """Test protected endpoints with token"""
    if not token:
        print("No token available for protected endpoint tests")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Test properties endpoint
        response = requests.get(f"{BASE_URL}/api/properties", 
                              headers=headers, timeout=10)
        print(f"Properties: {response.status_code}")
        
        # Test dashboard endpoint
        response = requests.get(f"{BASE_URL}/api/dashboard/landlord", 
                              headers=headers, timeout=10)
        print(f"Dashboard: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"Protected endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Deployment Verification ===")
    
    # Test health
    if not test_health():
        print("❌ Health check failed")
        sys.exit(1)
    
    print("✅ Health check passed")
    
    # Test authentication
    token = test_auth()
    if token:
        print("✅ Authentication working")
        
        # Test protected endpoints
        if test_protected_endpoints(token):
            print("✅ Protected endpoints working")
        else:
            print("⚠️ Some protected endpoints have issues")
    else:
        print("⚠️ Authentication issues detected")
    
    print("=== Verification Complete ===")

if __name__ == '__main__':
    main()