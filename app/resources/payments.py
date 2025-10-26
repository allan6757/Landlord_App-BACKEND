from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.models.user import User
from app.models.property import Property
from app.schemas.payment import PaymentSchema
from datetime import datetime
import uuid

payment_schema = PaymentSchema()

class PaymentList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.profile.role.value == 'landlord':
            payments = Payment.query.filter_by(landlord_id=user.profile.id).all()
        elif user.profile.role.value == 'tenant':
            payments = Payment.query.filter_by(tenant_id=user.profile.id).all()
        else:
            payments = Payment.query.all()

        return {'payments': [payment.to_dict() for payment in payments]}, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        data = request.get_json()
        errors = payment_schema.validate(data)
        if errors:
            return {'errors': errors}, 400
        
        # Verify property access
        property = Property.query.get_or_404(data['property_id'])
        if user.profile.role.value == 'tenant' and property.tenant_id != user.profile.id:
            return {'error': 'You can only make payments for your assigned properties'}, 403
        
        payment = Payment(
            amount=data['amount'],
            payment_method=PaymentMethod(data['payment_method']),
            description=data.get('description', 'Rent payment'),
            property_id=data['property_id'],
            tenant_id=user.profile.id if user.profile.role.value == 'tenant' else data.get('tenant_id'),
            landlord_id=property.landlord_id,
            reference=str(uuid.uuid4())[:8].upper()
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return {'payment': payment.to_dict()}, 201

class PaymentDetail(Resource):
    @jwt_required()
    def get(self, payment_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        payment = Payment.query.get_or_404(payment_id)
        
        # Check access permissions
        if (user.profile.role.value == 'tenant' and payment.tenant_id != user.profile.id) or \
           (user.profile.role.value == 'landlord' and payment.landlord_id != user.profile.id):
            return {'error': 'Access denied'}, 403
        
        return {'payment': payment.to_dict()}, 200
    
    @jwt_required()
    def put(self, payment_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        payment = Payment.query.get_or_404(payment_id)
        
        # Only landlords can update payment status
        if user.profile.role.value != 'landlord' or payment.landlord_id != user.profile.id:
            return {'error': 'Only property owner can update payment status'}, 403
        
        data = request.get_json()
        if 'status' in data:
            payment.status = PaymentStatus(data['status'])
            db.session.commit()
        
        return {'payment': payment.to_dict()}, 200