from marshmallow import Schema, fields

class ChatSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(required=True)
    sender_id = fields.Int(required=True)
    receiver_id = fields.Int(required=True)
    property_id = fields.Int()
    is_read = fields.Bool()
    created_at = fields.DateTime(dump_only=True)

class ChatCreateSchema(Schema):
    message = fields.Str(required=True)
    receiver_id = fields.Int(required=True)
    property_id = fields.Int()