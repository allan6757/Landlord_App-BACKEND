from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class ConversationSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(validate=validate.Length(max=200))
    last_message = fields.Str(dump_only=True)
    last_message_at = fields.DateTime(dump_only=True)
    initiator_id = fields.Int(required=True)
    participant_id = fields.Int(required=True)
    property_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    is_read = fields.Bool(dump_only=True)
    read_at = fields.DateTime(dump_only=True)
    conversation_id = fields.Int(required=True)
    sender_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class ConversationCreateSchema(Schema):
    participant_id = fields.Int(required=True)
    property_id = fields.Int(allow_none=True)
    title = fields.Str(validate=validate.Length(max=200))

class MessageCreateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    conversation_id = fields.Int(required=True)