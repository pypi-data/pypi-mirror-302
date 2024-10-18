from typing import TypeVar
from unittest.mock import Mock

from sqlalchemy import BinaryExpression
from sqlalchemy.sql.operators import in_op, eq

from base_kravata.template_repository import TemplateRepository


M = TypeVar("M")


class MockRepo(TemplateRepository[M]):
    """This is a class intented to be a MockRepository"""

    def __init__(self, model_cls):
        super().__init__(Mock(), model_cls)
        self.actions_performed = ""
        self.session = MockSession()

    def check_actions(self, expected):
        real = self.session.get_actions()
        assert real == expected, f"{real} not equal to {expected}"

    def check_queries(self, expected):
        reals = self.session.get_queries()
        assert len(expected) == len(
            reals
        ), f"Expected queries and reals are different size"
        for idx, query_obj in enumerate(reals):
            query = query_obj.get_actions()
            assert query == expected[idx], f"{query} not equal to {expected[idx]}"

    def get_queries(self):
        return self.session.get_queries()


class MockSession:
    """This is a class intented to be a Mock Repository session"""

    def __init__(self):
        self.__actions_performed = ""
        self.__queries = []

    def begin(self):
        self.__actions_performed += "begin:"  # pragma: no cover

    def add(self, data):
        if "Invalid" in data.__class__.__name__:
            raise TypeError
        self.__actions_performed += "add:"

    def query(self, model):
        self.__actions_performed += f"query({model.__name__}):"
        new_query = MockQuery(model)
        self.__queries.append(new_query)
        return new_query

    def commit(self):
        self.__actions_performed += "commit:"

    def rollback(self):
        self.__actions_performed += "rollback:"

    def get_actions(self):
        return self.__actions_performed.replace(":", " ").strip().split(" ")

    def get_queries(self):
        return self.__queries


class MockQuery:
    def __init__(self, model_cls, filters=None) -> None:
        self.filters = [] if filters is None else filters
        self.__filters_performed = ""
        self.__model_cls = model_cls
        self.result = [self.__model_cls()]

    def get(self, value):
        self.__filters_performed += f"get({value}):"
        if str(value) == "123e4567-e89b-12d3-a456-426614174000":
            return None
        return self.__model_cls()

    def get_actions(self):
        return self.__filters_performed.replace(":", " ").strip().split(" ")

    def filter(self, *args):
        new_filters = self.filters.copy()
        for filt in args:
            if isinstance(filt, BinaryExpression):
                filter_str = self.__get_filter_str(filt)
                self.__filters_performed += f"filter({filter_str}):"
                new_filters.append(filt)
            else:
                raise ValueError("Unexpected filter type")
        return self.__class__(self.__model_cls, filters=new_filters)

    def __get_filter_str(self, my_filter):
        left_value = my_filter.left.key
        right_value = my_filter.right.value
        if my_filter.operator is in_op:
            operator = "in"
        elif my_filter.operator == eq:
            operator = "=="
        else:
            raise NotImplementedError(f"Operator {my_filter.operator} not implemented")
        return f"{left_value}{operator}{right_value}"

    def all(self):
        return self.result

    def first(self):
        return self.result[0]
