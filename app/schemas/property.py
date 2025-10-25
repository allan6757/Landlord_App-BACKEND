from marshmallow import Schema, fields, validate

class PropertySchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str()
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    rent_amount = fields.Decimal(required=True, places=2)
    bedrooms = fields.Int()
    bathrooms = fields.Int()
    area = fields.Float()
    property_type = fields.Str()
    status = fields.Str(validate=validate.OneOf(['available', 'rented']))
    landlord_id = fields.Int(required=True)
    tenant_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)

class PropertyCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str()
    address = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    rent_amount = fields.Decimal(required=True, places=2)
    bedrooms = fields.Int()
    bathrooms = fields.Int()
    area = fields.Float()
    property_type = fields.Str()