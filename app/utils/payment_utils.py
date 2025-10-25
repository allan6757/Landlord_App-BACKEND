from datetime import date, timedelta
from app.models.payment import Payment, PaymentStatus

def get_overdue_payments():
    """Get all overdue payments that are still pending"""
    today = date.today()
    overdue_payments = Payment.query.filter(
        Payment.due_date < today,
        Payment.status == PaymentStatus.PENDING
    ).all()
    return overdue_payments

def get_upcoming_payments(days=7):
    """Get payments due within the next specified number of days"""
    today = date.today()
    future_date = today + timedelta(days=days)
    upcoming_payments = Payment.query.filter(
        Payment.due_date.between(today, future_date),
        Payment.status == PaymentStatus.PENDING
    ).all()
    return upcoming_payments

def calculate_total_revenue(landlord_id, start_date, end_date):
    """Calculate total revenue for a landlord within a date range"""
    payments = Payment.query.filter(
        Payment.landlord_id == landlord_id,
        Payment.status == PaymentStatus.COMPLETED,
        Payment.paid_date.between(start_date, end_date)
    ).all()
    
    total_revenue = sum(float(payment.amount) for payment in payments)
    return total_revenue

def get_payment_statistics(landlord_id=None, tenant_id=None):
    """Get payment statistics for landlord or tenant"""
    query = Payment.query
    
    if landlord_id:
        query = query.filter_by(landlord_id=landlord_id)
    if tenant_id:
        query = query.filter_by(tenant_id=tenant_id)
    
    total_payments = query.count()
    completed_payments = query.filter_by(status=PaymentStatus.COMPLETED).count()
    pending_payments = query.filter_by(status=PaymentStatus.PENDING).count()
    failed_payments = query.filter_by(status=PaymentStatus.FAILED).count()
    
    total_amount = sum(float(p.amount) for p in query.filter_by(status=PaymentStatus.COMPLETED).all())
    
    return {
        'total_payments': total_payments,
        'completed': completed_payments,
        'pending': pending_payments,
        'failed': failed_payments,
        'total_revenue': total_amount
    }

def check_payment_status(payment_id):
    """Check if a payment is overdue, upcoming, or on time"""
    payment = Payment.query.get(payment_id)
    if not payment:
        return None
    
    today = date.today()
    
    if payment.status == PaymentStatus.COMPLETED:
        return 'completed'
    elif payment.due_date < today:
        return 'overdue'
    elif payment.due_date <= today + timedelta(days=7):
        return 'upcoming'
    else:
        return 'scheduled'
