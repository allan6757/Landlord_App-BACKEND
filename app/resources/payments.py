from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Payment, db
from app.schemas.payment import PaymentSchema, PaymentCreateSchema

payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

@payments_bp.route('/', methods=['GET'])
@jwt_required()
def get_payments():
    user_id = get_jwt_identity()
    payments = Payment.query.filter_by(tenant_id=user_id).all()
    return PaymentSchema(many=True).dump(payments)

@payments_bp.route('/', methods=['POST'])
@jwt_required()
def create_payment():
    user_id = get_jwt_identity()
    schema = PaymentCreateSchema()
    data = schema.load(request.json)
    
    payment = Payment(**data, tenant_id=user_id)
    db.session.add(payment)
    db.session.commit()
    
    return PaymentSchema().dump(payment), 201