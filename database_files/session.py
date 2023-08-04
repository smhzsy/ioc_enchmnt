from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session():
    DATABASE_URL = "postgresql://postgres:password@localhost/ioc_enchmnt"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
