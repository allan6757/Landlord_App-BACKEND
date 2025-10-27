# Swagger/OpenAPI Configuration
# Provides interactive API documentation as required by capstone

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"  # Access Swagger UI at /api/docs
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Rental Platform API",
        "description": "RESTful API for property management system with landlord and tenant features",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@rentalplatform.com"
        }
    },
    "host": "localhost:5000",  # Will be overridden in production
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "tags": [
        {
            "name": "Authentication",
            "description": "User registration, login, and profile management"
        },
        {
            "name": "Users",
            "description": "User management operations (Admin only)"
        },
        {
            "name": "Properties",
            "description": "Property CRUD operations"
        },
        {
            "name": "Payments",
            "description": "Payment management and transactions"
        },
        {
            "name": "Chat",
            "description": "Messaging between landlords and tenants"
        }
    ],
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "is_active": {"type": "boolean"},
                "is_verified": {"type": "boolean"}
            }
        },
        "Property": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "address": {"type": "string"},
                "rent_amount": {"type": "number"},
                "is_occupied": {"type": "boolean"}
            }
        },
        "Payment": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "amount": {"type": "number"},
                "status": {"type": "string"},
                "transaction_id": {"type": "string"}
            }
        },
        "Error": {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    }
}
