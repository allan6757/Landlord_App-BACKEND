from datetime import datetime

def generate_receipt_data(payment):
    """Generate receipt data for a payment"""
    return {
        'receipt_id': f"RCPT-{payment.id:06d}",
        'issue_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'payment_date': payment.paid_date.strftime('%Y-%m-%d') if payment.paid_date else 'N/A',
        'tenant_name': f"{payment.tenant_user.user.first_name} {payment.tenant_user.user.last_name}",
        'landlord_name': f"{payment.landlord_user.user.first_name} {payment.landlord_user.user.last_name}",
        'property_address': payment.property.address,
        'amount': f"${payment.amount:.2f}",
        'payment_method': payment.payment_method.value if payment.payment_method else 'N/A',
        'transaction_id': payment.transaction_id or 'N/A',
        'period': f"{payment.due_date.strftime('%B %Y')}",
        'status': payment.status.value
    }

def format_receipt_text(receipt_data):
    """Format receipt data as plain text"""
    return f"""
    ================================================
                    PAYMENT RECEIPT
    ================================================
    
    Receipt ID:      {receipt_data['receipt_id']}
    Issue Date:      {receipt_data['issue_date']}
    
    ------------------------------------------------
                  PAYMENT DETAILS
    ------------------------------------------------
    
    Tenant:          {receipt_data['tenant_name']}
    Landlord:        {receipt_data['landlord_name']}
    Property:        {receipt_data['property_address']}
    
    Period:          {receipt_data['period']}
    Amount:          {receipt_data['amount']}
    Payment Date:    {receipt_data['payment_date']}
    Payment Method:  {receipt_data['payment_method']}
    Transaction ID:  {receipt_data['transaction_id']}
    Status:          {receipt_data['status'].upper()}
    
    ================================================
              Thank you for your payment!
    ================================================
    """

def format_receipt_html(receipt_data):
    """Format receipt data as HTML"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .receipt-header {{
                text-align: center;
                border-bottom: 2px solid #333;
                padding-bottom: 20px;
                margin-bottom: 20px;
            }}
            .receipt-body {{
                margin: 20px 0;
            }}
            .receipt-row {{
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }}
            .receipt-footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #333;
            }}
            .label {{
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="receipt-header">
            <h1>PAYMENT RECEIPT</h1>
            <p>Receipt ID: {receipt_data['receipt_id']}</p>
            <p>Issue Date: {receipt_data['issue_date']}</p>
        </div>
        
        <div class="receipt-body">
            <div class="receipt-row">
                <span class="label">Tenant:</span>
                <span>{receipt_data['tenant_name']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Landlord:</span>
                <span>{receipt_data['landlord_name']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Property:</span>
                <span>{receipt_data['property_address']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Period:</span>
                <span>{receipt_data['period']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Amount:</span>
                <span>{receipt_data['amount']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Payment Date:</span>
                <span>{receipt_data['payment_date']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Payment Method:</span>
                <span>{receipt_data['payment_method']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Transaction ID:</span>
                <span>{receipt_data['transaction_id']}</span>
            </div>
            <div class="receipt-row">
                <span class="label">Status:</span>
                <span>{receipt_data['status'].upper()}</span>
            </div>
        </div>
        
        <div class="receipt-footer">
            <p><strong>Thank you for your payment!</strong></p>
        </div>
    </body>
    </html>
    """
