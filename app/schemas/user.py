from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.Str(validate=validate.Length(max=20), allow_none=True)
    role = fields.Str(validate=validate.OneOf(['landlord', 'tenant', 'admin']))
    is_active = fields.Bool()
    profile_image = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.Str(validate=validate.Length(max=20), allow_none=True)
    role = fields.Str(validate=validate.OneOf(['landlord', 'tenant']), missing='tenant', allow_none=True)