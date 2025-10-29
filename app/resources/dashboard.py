from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Property, Payment, Conversation, db
from sqlalchemy import func
from datetime import datetime, timedelta

class LandlordDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role != 'landlord':
            return {'error': 'Landlord access required'}, 403
        
        # Get properties count
        total_properties = Property.query.filter_by(landlord_id=user.id).count()
        occupied_properties = Property.query.filter_by(
            landlord_id=user.id, 
            status='occupied'
        ).count()
        available_properties = Property.query.filter_by(
            landlord_id=user.id, 
            status='available'
        ).count()
        
        # Get payments data
        current_month = datetime.now().replace(day=1)
        monthly_revenue = db.session.query(func.sum(Payment.amount)).join(Property).filter(
            Property.landlord_id == user.id,
            Payment.status == 'completed',
            Payment.payment_date >= current_month
        ).scalar() or 0
        
        pending_payments = Payment.query.join(Property).filter(
            Property.landlord_id == user.id,
            Payment.status == 'pending'
        ).count()
        
        # Recent payments
        recent_payments = Payment.query.join(Property).filter(
            Property.landlord_id == user.id
        ).order_by(Payment.created_at.desc()).limit(5).all()
        
        # Unread messages count
        unread_messages = db.session.query(func.count()).select_from(Conversation).join(
            'messages'
        ).filter(
            Conversation.participant_id == user.id,
            'Message.is_read == False'
        ).scalar() or 0
        
        return {
            'summary': {
                'total_properties': total_properties,
                'occupied_properties': occupied_properties,
                'available_properties': available_properties,
                'monthly_revenue': float(monthly_revenue),
                'pending_payments': pending_payments,
                'unread_messages': unread_messages
            },
            'recent_payments': [payment.to_dict() for payment in recent_payments]
        }, 200

class TenantDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if user.role != 'tenant':
            return {'error': 'Tenant access required'}, 403
        
        # Get assigned property
        property = Property.query.filter_by(tenant_id=user.id).first()
        
        # Get payment history
        total_paid = db.session.query(func.sum(Payment.amount)).filter(
            Payment.tenant_id == user.id,
            Payment.status == 'completed'
        ).scalar() or 0
        
        pending_payments = Payment.query.filter_by(
            tenant_id=user.id,
            status='pending'
        ).count()
        
        # Recent payments
        recent_payments = Payment.query.filter_by(
            tenant_id=user.id
        ).order_by(Payment.created_at.desc()).limit(5).all()
        
        # Next rent due (assuming monthly rent)
        next_due_date = None
        if property and property.lease_start:
            # Calculate next month's rent due date
            today = datetime.now().date()
            next_due_date = today.replace(day=property.lease_start.day)
            if next_due_date <= today:
                if next_due_date.month == 12:
                    next_due_date = next_due_date.replace(year=next_due_date.year + 1, month=1)
                else:
                    next_due_date = next_due_date.replace(month=next_due_date.month + 1)
        
        # Unread messages count
        unread_messages = db.session.query(func.count()).select_from(Conversation).join(
            'messages'
        ).filter(
            Conversation.participant_id == user.id,
            'Message.is_read == False'
        ).scalar() or 0
        
        return {
            'summary': {
                'assigned_property': property.to_dict() if property else None,
                'total_paid': float(total_paid),
                'pending_payments': pending_payments,
                'next_due_date': next_due_date.isoformat() if next_due_date else None,
                'unread_messages': unread_messages
            },
            'recent_payments': [payment.to_dict() for payment in recent_payments]
        }, 200