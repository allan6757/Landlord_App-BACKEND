"""
Professional error handling utilities
"""

class AuthError:
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    EMAIL_EXISTS = "EMAIL_EXISTS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    SERVER_ERROR = "SERVER_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"

def create_error_response(message, code, status_code=400):
    """Create standardized error response"""
    return {
        "error": message,
        "code": code
    }, status_code

def create_success_response(data, message="Success", status_code=200):
    """Create standardized success response"""
    return {
        "success": True,
        "message": message,
        **data
    }, status_code