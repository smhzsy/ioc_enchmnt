from sqlalchemy import create_engine


def db_engine_create():
    """
    Database method for creating database engines.
    """
    engine = create_engine("postgresql://postgres:password@postgresql/ioc_enchmnt")
    return engine
