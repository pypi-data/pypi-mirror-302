from types import new_class
from typing import Callable, Generic, Type, TypeVar
from base_kravata.repository import BaseRepository
from base_kravata.model import Base
from sqlalchemy.orm import Session

M = TypeVar("M", bound=Base)


class TemplateRepository(BaseRepository, Generic[M]):
    """
    Template Repository, it extends of Base Repository
    It requires tht type of the model in order to initiate an child class
    """

    Model: M

    def __init__(self, session: Session, model_cls: Type[M]):
        super().__init__(session, model_cls)
        self.Model = model_cls


def create_repository(model_cls: Type[M]) -> Callable:
    """Factory Method to create a new Service with certain repository"""
    return new_class("Repository", (TemplateRepository[model_cls],))
