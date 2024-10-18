import uuid
from marshmallow import Schema, fields, validate


class ClientSchema(Schema):
    id = fields.UUID(required=True, default=uuid.uuid4)
    identification_type = fields.Str(
        required=True, validate=validate.OneOf(["nit", "cc", "passport"])
    )
    identification_number = fields.Str(required=True, validate=validate.Length(max=15))
    first_name = fields.Str(required=True, validate=validate.Length(max=15))
    middle_name = fields.Str(validate=validate.Length(max=15))
    surname = fields.Str(required=True, validate=validate.Length(max=15))
    last_name = fields.Str(validate=validate.Length(max=15))
    common_name = fields.Str(required=True, validate=validate.Length(max=15))
    register_date = fields.DateTime(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["active", "inactive"]))
