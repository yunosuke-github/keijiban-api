from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Length


class UserNestedSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    thread_id = fields.Int(required=True)
    content = fields.Str(required=True, validate=Length(max=1000))
    user_id = fields.Int(dump_only=True)
    likes = fields.Int(dump_only=True)
    dislikes = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user = fields.Nested(UserNestedSchema, dump_only=True)

    @validates_schema(pass_original=True)
    def validate_partial_update(self, data, original_data, **kwargs):
        if kwargs.get('partial') and not data:
            raise ValidationError('At least one field must be provided for update.')
