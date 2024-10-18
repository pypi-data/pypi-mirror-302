from marshmallow import Schema, fields, post_dump, pre_load

from base_kravata.utils import camel_to_snake, snake_to_camel


class CryptoAccount(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    auto_fuel = fields.Bool()
    hidden_on_ui = fields.Bool()
    assets = fields.List(fields.Dict())

    @pre_load
    def preprocess_input(self, data, **kwargs):
        # Convierte camelCase a snake_case
        return {camel_to_snake(key): value for key, value in data.items()}

    @post_dump
    def process_output(self, data, **kwargs):
        # Convierte snake_case a camelCase si necesitas exportarlo
        return {snake_to_camel(key): value for key, value in data.items()}
