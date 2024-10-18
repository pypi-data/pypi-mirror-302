from base_kravata.template_service import TemplateService
from marshmallow import Schema


class MockTemplateService(TemplateService):

    def __init__(self, model_cls):
        self.__actions_performed = ""
        self.__model_cls = model_cls

    def create(self, element):
        self.__actions_performed += f"create({element.__class__.__name__}):"
        if self.__is_value_in_attributes(element.__dict__, "invalid"):
            raise TypeError
        return element

    def __is_value_in_attributes(self, target_dict, expected_value):
        for _, value in target_dict.items():
            if isinstance(value, str):
                if expected_value.lower() in value.lower():
                    return True
            elif isinstance(value, Schema):  # pragma: no cover
                declared_fields_keys = value.declared_fields.keys()
                new_target = {k: v for k, v in value.__dict__.items() if k in declared_fields_keys}
                if self.__is_value_in_attributes(new_target, expected_value):
                    return True
        return False

    def get_by_id(self, element_id):  # pragma: no cover
        self.__actions_performed += f"getId({element_id}):"
        if element_id == "EXISTENT":
            return self.__model_cls()
        return None

    def get_by_params(self, filter_first=False, **kwargs):
        cardinality, formatted_str_kwargs = self.__process_action_str(filter_first, kwargs)
        self.__actions_performed += f"get{cardinality}({formatted_str_kwargs}):"
        if self.__is_value_in_attributes(kwargs, "EXISTENT"):
            return self.__process_existent_element(filter_first)
        return None

    # region get by params
    def __process_action_str(self, filter_first, kwargs):
        cardinality = "First" if filter_first else "All"
        formatted_str_kwargs = ", ".join(f"{key}={value}" for key, value in kwargs.items())
        return cardinality, formatted_str_kwargs

    def __process_existent_element(self, filter_first):
        res = [self.__model_cls()]
        if filter_first:
            res = res[0]
        return res

    # endregion

    def check_actions(self, expected):
        """
        Given a list of strings (expected actions) assert is equal to the actual performed actions
        """
        real = self.__get_actions()
        assert real == expected, f"{real} not equal to {expected}"

    def __get_actions(self):
        return self.__actions_performed.replace(":", " ").strip().split(" ")
