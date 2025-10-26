from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.property import Property
from app.models.user import User, UserProfile
from app.schemas.property import PropertySchema

property_schema = PropertySchema()

class PropertyList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.profile.role.value == 'landlord':
            properties = Property.query.filter_by(landlord_id=user.profile.id).all()
        elif user.profile.role.value == 'tenant':
            properties = Property.query.filter_by(tenant_id=user.profile.id).all()
        else:
            properties = Property.query.all()

        return {'properties': [prop.to_dict() for prop in properties]}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        if user.profile.role.value != 'landlord':
            return {'error': 'Only landlords can create properties'}, 403

        data = request.get_json()
        errors = property_schema.validate(data)
        if errors:
            return {'errors': errors}, 400

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

        return {'property': property.to_dict()}, 201

class PropertyDetail(Resource):
    @jwt_required()
    def get(self, property_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        property = Property.query.get_or_404(property_id)

        if not self._can_access_property(user, property):
            return {'error': 'Access denied'}, 403

        return {'property': property.to_dict()}, 200

    @jwt_required()
    def put(self, property_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        property = Property.query.get_or_404(property_id)

        if property.landlord_id != user.profile.id:
            return {'error': 'Only property owner can update'}, 403

        data = request.get_json()
        errors = property_schema.validate(data, partial=True)
        if errors:
            return {'errors': errors}, 400

        updatable_fields = ['title', 'description', 'address', 'city', 'state', 
                           'zip_code', 'property_type', 'monthly_rent', 
                           'security_deposit', 'bedrooms', 'bathrooms', 
                           'square_feet', 'amenities', 'status', 'tenant_id',
                           'lease_start', 'lease_end']

        for field in updatable_fields:
            if field in data:
                setattr(property, field, data[field])

        db.session.commit()
        return {'property': property.to_dict()}, 200

    @jwt_required()
    def delete(self, property_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        property = Property.query.get_or_404(property_id)

        if property.landlord_id != user.profile.id:
            return {'error': 'Only property owner can delete'}, 403

        db.session.delete(property)
        db.session.commit()

        return {'message': 'Property deleted successfully'}, 200

    def _can_access_property(self, user, property):
        if user.profile.role.value == 'admin':
            return True
        elif user.profile.role.value == 'landlord':
            return property.landlord_id == user.profile.id
        elif user.profile.role.value == 'tenant':
            return property.tenant_id == user.profile.id
        return False