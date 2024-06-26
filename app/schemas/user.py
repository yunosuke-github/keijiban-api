from marshmallow import Schema, fields, validates_schema, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates_schema(pass_original=True)
    def validate_partial_update(self, data, original_data, **kwargs):
        if kwargs.get('partial') and not data:
            raise ValidationError('At least one field must be provided for update.')
