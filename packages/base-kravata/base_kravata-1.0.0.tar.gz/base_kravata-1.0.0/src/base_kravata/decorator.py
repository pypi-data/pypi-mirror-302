from base_kravata.schema import generate_schema
from base_kravata.container import BaseContainer
from base_kravata.repository import BaseRepository
from flask import Request


def schema_controller(request:Request, model_in = None, model_out = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
                if model_in:
                    request.get_object = process_in(model_in, data)
                else:
                    request.get_object = data
                result = func(*args, **kwargs)
                if model_out:
                    result = process_out(model_out, result[0], result[1])
                return result
            except Exception as e:
                print(f"Error: {e}")
                return "Invalid request", 400
        return wrapper
    
    def process_in(model, data):
        in_schema = generate_schema(model)(session=BaseContainer.session)
        errors = in_schema.validate(data)
        if errors:
            raise ValueError(errors)
        data = in_schema.load(data)
        return data

    def process_out(model, data, code = None):
        out_schema = generate_schema(model)(session=BaseContainer.session)
        data = out_schema.dump(data)
        if code:
            result = data, code
        else:
            result = data
        return result

    return decorator