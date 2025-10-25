from marshmallow import ValidationError

def validate_positive_number(value):
    if value <= 0:
        raise ValidationError('Value must be positive')

def validate_rent_amount(value):
    if value < 1000:
        raise ValidationError('Rent amount must be at least 1000')

def validate_bedrooms(value):
    if value < 1 or value > 10:
        raise ValidationError('Bedrooms must be between 1 and 10')