# ============================================================================
# PAYMENT ENDPOINTS - Rent Payment Management with M-Pesa Integration
# ============================================================================
# Payment tracking and M-Pesa STK Push integration for rent payments
#
# ENDPOINTS:
# GET /api/payments - List payments (filtered by user role)
# POST /api/payments - Create payment and initiate M-Pesa STK Push
# GET /api/payments/<id> - Get payment details
# PUT /api/payments/<id> - Update payment status (landlord only)
# POST /api/payments/callback - M-Pesa callback endpoint
#
# ROLE-BASED FILTERING:
# - Landlord: Returns payments for their properties
# - Tenant: Returns their own payments
# - Admin: Returns all payments
#
# RESPONSE FORMAT:
# {
#   "payments": [
#     {
#       "id": 1,
#       "amount": 1500.00,
#       "status": "completed",  // pending/completed/failed
#       "due_date": "2024-01-15T00:00:00",
#       "property": {...},
#       "tenant": {...}
#     }
#   ]
# }
#
# M-PESA STK PUSH REQUEST:
# {
#   "property_id": 1,
#   "amount": 1500.00,
#   "phone_number": "254712345678",  // Kenyan phone format
#   "payment_method": "mpesa"
# }
#
# M-PESA FLOW:
# 1. POST /api/payments - Initiates STK Push to user's phone
# 2. User enters M-Pesa PIN on their phone
# 3. M-Pesa processes payment
# 4. M-Pesa sends callback to /api/payments/callback
# 5. Payment status updated to 'completed' or 'failed'
# 6. Email confirmation sent to tenant and landlord
# ============================================================================

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Payment, Property, User, db
from app.schemas.payment import PaymentSchema, PaymentCreateSchema
from app.utils.payments import MPesaService
from app.utils.email import send_payment_confirmation
from datetime import datetime
import uuid
from marshmallow import ValidationError

class PaymentList(Resource):
    """Payment list endpoint - Get all payments or create new payment"""
    @jwt_required()  # Requires JWT token in Authorization header
    def get(self):
        """Get payments filtered by user role
        Landlords see payments for their properties, tenants see their payments
        """
        user_id = get_jwt_identity()  # Extract user ID from JWT token
        user = User.query.get_or_404(user_id)
        
        # Filter payments based on user role
        if user.role == 'landlord':
            # Landlords see payments for properties they own
            payments = Payment.query.join(Property).filter(Property.landlord_id == user.id).all()
        elif user.role == 'tenant':
            # Tenants see their own payments
            payments = Payment.query.filter_by(tenant_id=user.id).all()
        else:
            # Admins see all payments
            payments = Payment.query.all()
        
        # Return payments array as expected by frontend
        return {'payments': [payment.to_dict() for payment in payments]}, 200

    @jwt_required()  # Requires JWT token
    def post(self):
        """Create new payment and initiate M-Pesa STK Push
        Sends payment prompt to user's phone for M-Pesa payment
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        # Validate request data
        schema = PaymentCreateSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return {'errors': err.messages}, 400
        
        property = Property.query.get_or_404(data['property_id'])
        
        # Verify tenant can pay for this property
        if user.role == 'tenant' and property.tenant_id != user.id:
            return {'error': 'You can only pay for your assigned property'}, 403
        
        # Create payment record
        payment = Payment(
            amount=data['amount'],
            payment_date=datetime.utcnow(),  # Used as due_date
            payment_method=data.get('payment_method', 'mpesa'),
            property_id=data['property_id'],
            tenant_id=user.id,
            reference=str(uuid.uuid4()),  # Unique payment reference
            phone_number=data.get('phone_number')
        )
        
        db.session.add(payment)
        db.session.commit()
        
        # Initiate M-Pesa STK Push if payment method is M-Pesa
        if payment.payment_method.value == 'mpesa' and payment.phone_number:
            mpesa = MPesaService()
            # Send STK Push to user's phone
            result = mpesa.initiate_payment(
                payment.phone_number,
                payment.amount,
                payment.reference
            )
            
            if 'CheckoutRequestID' in result:
                # Store M-Pesa checkout ID for callback matching
                payment.mpesa_checkout_id = result['CheckoutRequestID']
                db.session.commit()
            elif 'error' in result:
                # Mark payment as failed if STK Push fails
                payment.status = 'failed'
                db.session.commit()
                return {'error': result['error']}, 400
        
        return {'payment': payment.to_dict()}, 201

class PaymentDetail(Resource):
    """Payment detail endpoint - Get or update specific payment"""
    @jwt_required()
    def get(self, payment_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        payment = Payment.query.get_or_404(payment_id)
        
        # Check access permissions
        if user.role == 'tenant' and payment.tenant_id != user.id:
            return {'error': 'Access denied'}, 403
        elif user.role == 'landlord' and payment.property.landlord_id != user.id:
            return {'error': 'Access denied'}, 403
        
        return {'payment': payment.to_dict()}, 200
    
    @jwt_required()
    def put(self, payment_id):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        payment = Payment.query.get_or_404(payment_id)
        
        # Only landlords can update payment status
        if user.role != 'landlord' or payment.property.landlord_id != user.id:
            return {'error': 'Only property owner can update payment status'}, 403
        
        data = request.json
        if 'status' in data:
            payment.status = data['status']
            
            # Send confirmation email if payment is completed
            if payment.status.value == 'completed':
                send_payment_confirmation(payment)
        
        db.session.commit()
        return {'payment': payment.to_dict()}, 200

class PaymentCallback(Resource):
    """M-Pesa callback endpoint - Receives payment status from M-Pesa"""
    def post(self):
        """Process M-Pesa callback and update payment status
        Called by M-Pesa after user completes or cancels payment
        """
        data = request.json
        
        # Parse M-Pesa callback data
        if 'Body' in data and 'stkCallback' in data['Body']:
            callback_data = data['Body']['stkCallback']
            checkout_id = callback_data.get('CheckoutRequestID')
            
            # Find payment by M-Pesa checkout ID
            payment = Payment.query.filter_by(mpesa_checkout_id=checkout_id).first()
            if payment:
                # ResultCode 0 means success
                if callback_data.get('ResultCode') == 0:
                    payment.status = 'completed'
                    # Send email confirmation to tenant and landlord
                    send_payment_confirmation(payment)
                else:
                    # Payment failed or cancelled
                    payment.status = 'failed'
                
                db.session.commit()
        
        return {'message': 'Callback processed'}, 200