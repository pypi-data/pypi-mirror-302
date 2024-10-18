from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class BaseContainer(containers.DeclarativeContainer):
    # Configuración
    config = providers.Configuration()

    # Base de datos
    engine = providers.Singleton(
        create_engine,
        config.database_url
    )
    session_factory = providers.Singleton(
        sessionmaker,
        bind=engine
    )
    session = providers.Singleton(
        session_factory
    )