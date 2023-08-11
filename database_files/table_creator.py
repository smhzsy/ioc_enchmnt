from database_files.engine_creator import db_engine_create
from database_files.model import Base

engine = db_engine_create()


def create_tables():
    """
    Database method to create Database tables.
    """
    Base.metadata.create_all(engine)
