from marshmallow import Schema, fields, validate

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Decimal(required=True, places=2)
    payment_date = fields.DateTime(required=True)
    payment_method = fields.Str()
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'failed']))
    reference = fields.Str()
    property_id = fields.Int(required=True)
    tenant_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

class PaymentCreateSchema(Schema):
    amount = fields.Decimal(required=True, places=2)
    payment_date = fields.DateTime(required=True)
    payment_method = fields.Str()
    reference = fields.Str()
    property_id = fields.Int(required=True)