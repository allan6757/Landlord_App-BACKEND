from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from app.models.user import UserRole

class UserProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    phone = fields.Str(validate=validate.Length(max=20))
    address = fields.Str()
    role = fields.Str(validate=validate.OneOf([role.value for role in UserRole]))
    date_of_birth = fields.Date()
    emergency_contact = fields.Str(validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    first_name = fields.Str(required=True, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(max=50))
    is_active = fields.Bool(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    profile = fields.Nested(UserProfileSchema, dump_only=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)