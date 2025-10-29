from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Property, User, db
from app.schemas.property import PropertySchema, PropertyCreateSchema
from app.utils.cloudinary import upload_image, delete_image
from marshmallow import ValidationError

class PropertyList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        if user.role == 'landlord':
            properties = Property.query.filter_by(landlord_id=user.id).all()
        elif user.role == 'tenant':
            properties = Property.query.filter_by(tenant_id=user.id).all()
        else:
            properties = Property.query.all()

        return {'properties': [prop.to_dict() for prop in properties]}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)

        if user.role != 'landlord':
            return {'error': 'Only landlords can create properties'}, 403

        schema = PropertyCreateSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {'errors': err.messages}, 400

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
            landlord_id=user.id
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

        if property.landlord_id != user.id:
            return {'error': 'Only property owner can update'}, 403

        data = request.json
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

        if property.landlord_id != user.id:
            return {'error': 'Only property owner can delete'}, 403

        # Delete associated images from Cloudinary
        if property.images:
            for image in property.images:
                if 'public_id' in image:
                    delete_image(image['public_id'])

        db.session.delete(property)
        db.session.commit()

        return {'message': 'Property deleted successfully'}, 200

    def _can_access_property(self, user, property):
        if user.role == 'admin':
            return True
        elif user.role == 'landlord':
            return property.landlord_id == user.id
        elif user.role == 'tenant':
            return property.tenant_id == user.id
        return False

class PropertyImages(Resource):
    @jwt_required()
    def post(self, property_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        property = Property.query.get_or_404(property_id)

        if property.landlord_id != user.id:
            return {'error': 'Only property owner can upload images'}, 403

        if 'image' not in request.files:
            return {'error': 'No image file provided'}, 400

        file = request.files['image']
        result = upload_image(file, folder=f"properties/{property_id}")
        
        if 'error' in result:
            return {'error': result['error']}, 400

        # Add image to property
        if not property.images:
            property.images = []
        
        property.images.append(result)
        db.session.commit()

        return {'image': result}, 201