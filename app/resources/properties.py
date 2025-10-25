from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Property, User, db
from app.schemas.property import PropertySchema

properties_bp = Blueprint('properties', __name__, url_prefix='/api/properties')
property_schema = PropertySchema()

@properties_bp.route('/', methods=['GET'])
@jwt_required()
def get_properties():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    if user.role == 'landlord':
        properties = Property.query.filter_by(landlord_id=user.id).all()
    elif user.role == 'tenant':
        properties = Property.query.filter_by(tenant_id=user.id).all()
    else:
        properties = Property.query.all()

    return {'properties': [prop.to_dict() for prop in properties]}, 200

@properties_bp.route('/', methods=['POST'])
@jwt_required()
def create_property():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    if user.role != 'landlord':
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
        landlord_id=user.id
    )

    db.session.add(property)
    db.session.commit()

    return {'property': property.to_dict()}, 201

@properties_bp.route('/<int:property_id>', methods=['GET'])
@jwt_required()
def get_property(property_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    property = Property.query.get_or_404(property_id)

    if not _can_access_property(user, property):
        return {'error': 'Access denied'}, 403

    return {'property': property.to_dict()}, 200

@properties_bp.route('/<int:property_id>', methods=['PUT'])
@jwt_required()
def update_property(property_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    property = Property.query.get_or_404(property_id)

    if property.landlord_id != user.id:
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

@properties_bp.route('/<int:property_id>', methods=['DELETE'])
@jwt_required()
def delete_property(property_id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    property = Property.query.get_or_404(property_id)

    if property.landlord_id != user.id:
        return {'error': 'Only property owner can delete'}, 403

    db.session.delete(property)
    db.session.commit()

    return {'message': 'Property deleted successfully'}, 200

def _can_access_property(user, property):
    if user.role == 'admin':
        return True
    elif user.role == 'landlord':
        return property.landlord_id == user.id
    elif user.role == 'tenant':
        return property.tenant_id == user.id
    return False