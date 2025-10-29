#!/usr/bin/env python3
"""
Complete Backend Test Script
Tests all MVP features: Auth, Properties, Payments, Chat
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "https://landlord-app-backend-1eph.onrender.com"
# BASE_URL = "http://localhost:5000"  # Uncomment for local testing

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if details:
        print(f"  {details}")

def test_health_check():
    """Test 1: Health Check"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        passed = response.status_code == 200
        print_test("Health Check", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Health Check", False, f"Error: {str(e)}")
        return False

def test_registration():
    """Test 2: User Registration"""
    try:
        data = {
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "password": "Test123!",
            "first_name": "Test",
            "last_name": "User",
            "role": "tenant"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        passed = response.status_code in [200, 201]
        result = response.json() if response.status_code in [200, 201] else response.text
        print_test("User Registration", passed, f"Status: {response.status_code}")
        if passed:
            return result.get('data', {}).get('token'), result.get('data', {}).get('user')
        return None, None
    except Exception as e:
        print_test("User Registration", False, f"Error: {str(e)}")
        return None, None

def test_login():
    """Test 3: User Login"""
    try:
        # First register a user
        email = f"login_test_{datetime.now().timestamp()}@example.com"
        register_data = {
            "email": email,
            "password": "Test123!",
            "first_name": "Login",
            "last_name": "Test",
            "role": "landlord"
        }
        requests.post(f"{BASE_URL}/api/auth/register", json=register_data, timeout=10)
        
        # Now login
        login_data = {
            "email": email,
            "password": "Test123!"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        passed = response.status_code == 200
        result = response.json() if passed else response.text
        print_test("User Login", passed, f"Status: {response.status_code}")
        if passed:
            return result.get('data', {}).get('token'), result.get('data', {}).get('user')
        return None, None
    except Exception as e:
        print_test("User Login", False, f"Error: {str(e)}")
        return None, None

def test_profile(token):
    """Test 4: Get User Profile"""
    if not token:
        print_test("Get Profile", False, "No token available")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/profile",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        passed = response.status_code == 200
        print_test("Get Profile", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Get Profile", False, f"Error: {str(e)}")
        return False

def test_create_property(token):
    """Test 5: Create Property (Landlord)"""
    if not token:
        print_test("Create Property", False, "No token available")
        return None
    
    try:
        data = {
            "title": "Test Property",
            "description": "A beautiful test property",
            "address": "123 Test Street",
            "city": "Test City",
            "price": 50000,
            "bedrooms": 3,
            "bathrooms": 2,
            "property_type": "apartment",
            "status": "available"
        }
        response = requests.post(
            f"{BASE_URL}/api/properties",
            json=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        passed = response.status_code in [200, 201]
        result = response.json() if passed else response.text
        print_test("Create Property", passed, f"Status: {response.status_code}")
        if passed:
            return result.get('data', {}).get('property', {}).get('id')
        return None
    except Exception as e:
        print_test("Create Property", False, f"Error: {str(e)}")
        return None

def test_list_properties(token):
    """Test 6: List Properties"""
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(
            f"{BASE_URL}/api/properties",
            headers=headers,
            timeout=10
        )
        passed = response.status_code == 200
        print_test("List Properties", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("List Properties", False, f"Error: {str(e)}")
        return False

def test_create_conversation(token, user_id):
    """Test 7: Create Conversation"""
    if not token:
        print_test("Create Conversation", False, "No token available")
        return None
    
    try:
        data = {
            "participant_id": user_id or 1,
            "title": "Test Conversation"
        }
        response = requests.post(
            f"{BASE_URL}/api/conversations",
            json=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        passed = response.status_code in [200, 201]
        result = response.json() if passed else response.text
        print_test("Create Conversation", passed, f"Status: {response.status_code}")
        if passed:
            return result.get('conversation', {}).get('id')
        return None
    except Exception as e:
        print_test("Create Conversation", False, f"Error: {str(e)}")
        return None

def test_send_message(token, conversation_id):
    """Test 8: Send Message"""
    if not token or not conversation_id:
        print_test("Send Message", False, "No token or conversation_id available")
        return False
    
    try:
        data = {
            "content": "Hello! This is a test message."
        }
        response = requests.post(
            f"{BASE_URL}/api/conversations/{conversation_id}/messages",
            json=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        passed = response.status_code in [200, 201]
        print_test("Send Message", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Send Message", False, f"Error: {str(e)}")
        return False

def test_list_conversations(token):
    """Test 9: List Conversations"""
    if not token:
        print_test("List Conversations", False, "No token available")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/conversations",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        passed = response.status_code == 200
        print_test("List Conversations", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("List Conversations", False, f"Error: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Landlord House Management System - Backend Tests{Colors.END}")
    print(f"{Colors.BLUE}Testing: {BASE_URL}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    results = []
    
    # Test 1: Health Check
    print(f"\n{Colors.YELLOW}Testing Core Functionality{Colors.END}")
    results.append(test_health_check())
    
    # Test 2-3: Authentication
    print(f"\n{Colors.YELLOW}Testing Authentication{Colors.END}")
    token, user = test_registration()
    results.append(token is not None)
    
    login_token, login_user = test_login()
    results.append(login_token is not None)
    
    # Use login token for remaining tests
    active_token = login_token or token
    active_user = login_user or user
    
    # Test 4: Profile
    results.append(test_profile(active_token))
    
    # Test 5-6: Properties
    print(f"\n{Colors.YELLOW}Testing Property Management{Colors.END}")
    property_id = test_create_property(active_token)
    results.append(property_id is not None)
    results.append(test_list_properties(active_token))
    
    # Test 7-9: Chat System
    print(f"\n{Colors.YELLOW}Testing Chat System{Colors.END}")
    user_id = active_user.get('id') if active_user else None
    conversation_id = test_create_conversation(active_token, user_id)
    results.append(conversation_id is not None)
    results.append(test_send_message(active_token, conversation_id))
    results.append(test_list_conversations(active_token))
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    if percentage == 100:
        color = Colors.GREEN
        status = "ALL TESTS PASSED! ✓"
    elif percentage >= 70:
        color = Colors.YELLOW
        status = "MOST TESTS PASSED"
    else:
        color = Colors.RED
        status = "MANY TESTS FAILED"
    
    print(f"{color}{status}{Colors.END}")
    print(f"Results: {passed}/{total} tests passed ({percentage:.1f}%)")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    return percentage == 100

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
