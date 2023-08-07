from sqlalchemy.orm import sessionmaker

from database_files.engine_creator import db_engine_create


def create_session():
    """
    Database method for creating database sessions.
    """
    engine = db_engine_create()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
