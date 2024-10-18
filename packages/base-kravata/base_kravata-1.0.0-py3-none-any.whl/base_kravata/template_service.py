from abc import ABC
from types import new_class
from typing import Callable, Generic, Type, TypeVar
import uuid

from base_kravata.template_repository import TemplateRepository
from base_kravata.exceptions import DBErrorWithRollback, InvalidModel

M = TypeVar("M")
R = TypeVar("R", bound=TemplateRepository[M])


class TemplateService(ABC, Generic[R]):
    """
    Template Service with creation method called Create
    In order to use, you have to inherit this class specifying the type of the repo
    """

    def __init__(self, repo: R):
        self.repository = repo

    def create(self, element: M):
        """
        Create method, receive an element and returns the same element if everything is correct
        """
        self.__validate_instance(element)
        return self.__try_run_db_transaction(element)

    # region
    def __validate_instance(self, element: M) -> None:
        model_cls = self.repository.Model
        if not isinstance(element, model_cls):
            raise InvalidModel(f"Expected {model_cls.__name__}, got {type(element).__name__}")

    def __try_run_db_transaction(self, element) -> M:
        try:
            return self.__run_db_transaction(element)
        except Exception as e:
            self.repository.session.rollback()
            raise DBErrorWithRollback from e

    def __run_db_transaction(self, acc) -> M:
        acc = self.repository.save(acc)
        self.repository.session.commit()
        return acc

    # endregion

    def get_by_id(self, element_id: uuid.UUID):
        """
        Get by Id method, receive an element id and returns the element if exists, None otherwise
        """
        if not isinstance(element_id, uuid.UUID):
            raise InvalidModel("Not uuid given")
        return self.repository.get_by_id(element_id)

    def get_by_params(self, filter_first=False, **kwargs):
        """
        Get by params, it has flag filter_first if you only want the first element.
        The params should be sent as kwargs
        """
        if filter_first:
            return self.repository.filter_first(**kwargs)
        return self.repository.filter_all(**kwargs)


def create_service(repository_cls: Type[R]) -> Callable:
    """Factory Method to create a new Service with certain repository"""
    return new_class("Service", (TemplateService[repository_cls],))
