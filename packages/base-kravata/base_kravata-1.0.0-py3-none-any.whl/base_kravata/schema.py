import re, typing
from marshmallow import post_dump, pre_dump, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from base_kravata.utils import camel_to_snake, snake_to_camel


# se crea una funcion generadora del generador de clases
def generate_schema(par_model):
    class DynamicModelSchema(SQLAlchemyAutoSchema):
        class Meta:
            model = par_model
            include_fk = True
            # include_relationships = True
            load_instance = True  # Para cargar instancias de modelos SQLAlchemy

        @pre_load
        def cus_load(self, data, session=None, *args, **kwargs):
            data = {camel_to_snake(key): value for key, value in data.items()}
            return data

        @post_dump
        def cus_dump(self, obj: typing.Any, *, many: bool | None = None):
            return {snake_to_camel(key): value for key, value in obj.items()}

    return DynamicModelSchema


class DynamicMetaSchema(SQLAlchemyAutoSchema):
    def __new__(cls, par_model, *args, **kwargs):
        # Modificar la clase Meta dinámicamente en el momento de la creación de la clase
        class Meta:
            model = par_model
            load_instance = True

        # Añadir la clase Meta a la clase actual
        cls.Meta = Meta

        # Crear una instancia de la clase usando el método original
        return super().__new__(cls)
