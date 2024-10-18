from marshmallow import Schema, fields


class UserSchema (Schema):

    id = fields.UUID()
    unique_code  = fields.Str(required=True)
    status = fields.Str(required=True)
    register_date = fields.DateTime()
    client_id = fields.UUID()