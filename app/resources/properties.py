# Property Management Resources
# Handles CRUD operations for properties with RBAC and pagination

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.property import Property
from app.models.user import User, UserProfile, UserRole
from app.schemas.property import PropertySchema
from app.utils.pagination import paginate_query
from app.utils.decorators import role_required, landlord_required
from flasgger import swag_from

property_schema = PropertySchema()

class PropertyList(Resource):
    @jwt_required()
    def get(self):
        """
        Get list of properties with pagination (role-based filtering)
        ---
        tags:
          - Properties
        security:
          - Bearer: []
        parameters:
          - name: page
            in: query
            type: integer
            default: 1
            description: Page number
          - name: per_page
            in: query
            type: integer
            default: 10
            description: Items per page (max 100)
        responses:
          200:
            description: List of properties with pagination
          401:
            description: Unauthorized
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        # Filter properties based on user role
        if user.profile.role == UserRole.LANDLORD:
            # Landlords see only their properties
            query = Property.query.filter_by(landlord_id=user.profile.id)
        elif user.profile.role == UserRole.TENANT:
            # Tenants see only their assigned properties
            query = Property.query.filter_by(tenant_id=user.profile.id)
        else:
            # Admins see all properties
            query = Property.query

        # Apply pagination
        result = paginate_query(query, property_schema)
        return result, 200

    @jwt_required()
    @landlord_required  # Only landlords can create properties
    def post(self):
        """
        Create a new property (Landlords only)
        ---
        tags:
          - Properties
        security:
          - Bearer: []
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - title
                - address
                - city
                - state
                - zip_code
                - property_type
                - monthly_rent
              properties:
                title:
                  type: string
                description:
                  type: string
                address:
                  type: string
                city:
                  type: string
                state:
                  type: string
                zip_code:
                  type: string
                property_type:
                  type: string
                monthly_rent:
                  type: number
                security_deposit:
                  type: number
                bedrooms:
                  type: integer
                bathrooms:
                  type: number
                square_feet:
                  type: integer
                amenities:
                  type: string
        responses:
          201:
            description: Property created successfully
          400:
            description: Validation error
          403:
            description: Access denied (not a landlord)
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        data = request.get_json()
        
        # Validate input data
        errors = property_schema.validate(data)
        if errors:
            return {'errors': errors}, 400

        try:
            # Create new property
            property = Property(
                title=data['title'],
                description=data.get('description'),
                address=data['address'],
                city=data['city'],
                state=data['state'],
                zip_code=data['zip_code'],
                property_type=data['property_type'],
                monthly_rent=data['monthly_rent'],
                security_deposit=data.get('security_deposit', 0),
                bedrooms=data.get('bedrooms'),
                bathrooms=data.get('bathrooms'),
                square_feet=data.get('square_feet'),
                amenities=data.get('amenities'),
                landlord_id=user.profile.id
            )

            db.session.add(property)
            db.session.commit()

            return {
                'message': 'Property created successfully',
                'property': property.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create property: {str(e)}'}, 500

class PropertyDetail(Resource):
    @jwt_required()
    def get(self, property_id):
        """
        Get property details by ID
        ---
        tags:
          - Properties
        security:
          - Bearer: []
        parameters:
          - name: property_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Property details
          403:
            description: Access denied
          404:
            description: Property not found
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        property = Property.query.get_or_404(property_id)

        # Check if user can access this property
        if not self._can_access_property(user, property):
            return {'error': 'Access denied to this property'}, 403

        return {'property': property.to_dict()}, 200

    @jwt_required()
    def put(self, property_id):
        """
        Update property details (Owner only)
        ---
        tags:
          - Properties
        security:
          - Bearer: []
        parameters:
          - name: property_id
            in: path
            type: integer
            required: true
          - name: body
            in: body
            schema:
              type: object
              properties:
                title:
                  type: string
                description:
                  type: string
                monthly_rent:
                  type: number
                status:
                  type: string
        responses:
          200:
            description: Property updated successfully
          403:
            description: Not authorized
          404:
            description: Property not found
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        property = Property.query.get_or_404(property_id)

        # Only property owner can update
        if property.landlord_id != user.profile.id:
            return {'error': 'Only property owner can update'}, 403

        data = request.get_json()
        
        # Validate partial data
        errors = property_schema.validate(data, partial=True)
        if errors:
            return {'errors': errors}, 400

        try:
            # List of fields that can be updated
            updatable_fields = ['title', 'description', 'address', 'city', 'state', 
                               'zip_code', 'property_type', 'monthly_rent', 
                               'security_deposit', 'bedrooms', 'bathrooms', 
                               'square_feet', 'amenities', 'status', 'tenant_id',
                               'lease_start', 'lease_end']

            # Update only provided fields
            for field in updatable_fields:
                if field in data:
                    setattr(property, field, data[field])

            db.session.commit()
            
            return {
                'message': 'Property updated successfully',
                'property': property.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to update property: {str(e)}'}, 500

    @jwt_required()
    def delete(self, property_id):
        """
        Delete property (Owner only)
        ---
        tags:
          - Properties
        security:
          - Bearer: []
        parameters:
          - name: property_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Property deleted successfully
          403:
            description: Not authorized
          404:
            description: Property not found
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        property = Property.query.get_or_404(property_id)

        # Only property owner can delete
        if property.landlord_id != user.profile.id:
            return {'error': 'Only property owner can delete'}, 403

        try:
            db.session.delete(property)
            db.session.commit()

            return {'message': 'Property deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to delete property: {str(e)}'}, 500

    def _can_access_property(self, user, property):
        """
        Check if user has permission to access property
        
        Args:
            user: User object
            property: Property object
            
        Returns:
            Boolean indicating access permission
        """
        # Admin can access all properties
        if user.profile.role == UserRole.ADMIN:
            return True
        # Landlord can access their own properties
        elif user.profile.role == UserRole.LANDLORD:
            return property.landlord_id == user.profile.id
        # Tenant can access their assigned properties
        elif user.profile.role == UserRole.TENANT:
            return property.tenant_id == user.profile.id
        return False