from logging import info

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import environment
from app.models.product_model import ProductModel

DATABASE_URL = f'sqlite:///{environment.db_name}'


class DatabaseConnection:
    engine = create_engine(DATABASE_URL, echo=True)
    metadata = MetaData()
    session_local = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    @staticmethod
    def get_session():
        return DatabaseConnection.session_local()

    @classmethod
    def init_database_connection(cls):
        cls.metadata.reflect(bind=cls.engine)

        if 'catalog' not in cls.metadata.tables:
            info("The table 'catalog' does not exist in the database.")
            ProductModel.metadata.create_all(bind=cls.engine)
