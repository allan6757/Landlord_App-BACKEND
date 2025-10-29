from marshmallow import Schema, fields, validate

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Decimal(required=True, validate=validate.Range(min=0))
    payment_date = fields.DateTime(dump_only=True)
    payment_method = fields.Str(validate=validate.OneOf(['mpesa', 'bank', 'cash', 'card']))
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'failed', 'cancelled']))
    reference = fields.Str(dump_only=True)
    phone_number = fields.Str()
    property_id = fields.Int(required=True)
    tenant_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class PaymentCreateSchema(Schema):
    amount = fields.Decimal(required=True, validate=validate.Range(min=0))
    payment_method = fields.Str(validate=validate.OneOf(['mpesa', 'bank', 'cash', 'card']))
    property_id = fields.Int(required=True)
    phone_number = fields.Str(validate=validate.Length(min=10, max=15))