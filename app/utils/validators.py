import re
from datetime import datetime
from marshmallow import ValidationError

def validate_zip_code(zip_code):
    pattern = r'^\d{5}(-\d{4})?$'
    return re.match(pattern, zip_code) is not None

def validate_phone(phone):
    pattern = r'^+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def validate_date_range(start_date, end_date):
    if not start_date or not end_date:
        return True
    return start_date < end_date

def validate_rent_amount(amount):
    return amount >= 0

def sanitize_text(text):
    if not text:
        return text
    return text.strip()

def validate_positive_number(value):
    if value <= 0:
        raise ValidationError('Value must be positive')

def validate_bedrooms(value):
    if value < 1 or value > 10:
        raise ValidationError('Bedrooms must be between 1 and 10')