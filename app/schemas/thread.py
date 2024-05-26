from marshmallow import Schema, fields, validates_schema, ValidationError


class ThreadSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=lambda x: len(x) <= 50)
    category = fields.Str(validate=lambda x: len(x) <= 10)
    description = fields.Str(validate=lambda x: len(x) <= 400)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    views = fields.Int(dump_only=True)

    @validates_schema(pass_original=True)
    def validate_partial_update(self, data, original_data, **kwargs):
        if kwargs.get('partial') and not data:
            raise ValidationError('At least one field must be provided for update.')
