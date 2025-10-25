from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import date

class PropertySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=200))
    description = fields.Str()
    address = fields.Str(required=True)
    city = fields.Str(required=True, validate=validate.Length(max=100))
    state = fields.Str(required=True, validate=validate.Length(max=50))
    zip_code = fields.Str(required=True, validate=validate.Length(max=20))
    property_type = fields.Str(required=True, validate=validate.OneOf(['apartment', 'house', 'condo', 'townhouse']))
    status = fields.Str(validate=validate.OneOf(['available', 'occupied', 'maintenance', 'unavailable']))

    monthly_rent = fields.Float(required=True, validate=validate.Range(min=0))
    security_deposit = fields.Float(validate=validate.Range(min=0))
    bedrooms = fields.Int(validate=validate.Range(min=0))
    bathrooms = fields.Float(validate=validate.Range(min=0))
    square_feet = fields.Int(validate=validate.Range(min=0))
    amenities = fields.Str()

    landlord_id = fields.Int(dump_only=True)
    tenant_id = fields.Int(allow_none=True)
    lease_start = fields.Date()
    lease_end = fields.Date()

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data.get('lease_start') and data.get('lease_end'):
            if data['lease_start'] >= data['lease_end']:
                raise ValidationError('Lease end date must be after start date')