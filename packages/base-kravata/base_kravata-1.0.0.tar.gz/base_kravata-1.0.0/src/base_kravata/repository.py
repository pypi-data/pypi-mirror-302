from base_kravata.utils import camel_to_snake


class BaseRepository:

    def __init__(self, session, model):
        self.session = session()
        self.model = model

    def get_by_id(self, id):
        result = self.create_query().get(id)
        return result

    def create_query(self):
        return self.session.query(self.model)

    def save(self, data):
        if data.id is None:
            self.session.add(data)
        return data

    def set_filter_query(self, **kwargs):
        query = self.create_query()
        for attribute, value in kwargs.items():
            snake_case_attribute = camel_to_snake(attribute)
            query = query.filter(getattr(self.model, snake_case_attribute) == value)
        return query

    def filter_first(self, **kwargs):
        return self.set_filter_query(**kwargs).first()

    def filter_all(self, **kwargs):
        return self.set_filter_query(**kwargs).all()
