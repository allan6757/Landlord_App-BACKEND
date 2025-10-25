from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Property, db
from app.schemas.property import PropertySchema, PropertyCreateSchema

properties_bp = Blueprint('properties', __name__, url_prefix='/api/properties')

@properties_bp.route('/', methods=['GET'])
def get_properties():
    properties = Property.query.filter_by(status='available').all()
    return PropertySchema(many=True).dump(properties)

@properties_bp.route('/', methods=['POST'])
@jwt_required()
def create_property():
    user_id = get_jwt_identity()
    schema = PropertyCreateSchema()
    data = schema.load(request.json)
    
    property = Property(**data, landlord_id=user_id)
    db.session.add(property)
    db.session.commit()
    
    return PropertySchema().dump(property), 201

@properties_bp.route('/<int:property_id>', methods=['GET'])
def get_property(property_id):
    property = Property.query.get_or_404(property_id)
    return PropertySchema().dump(property)