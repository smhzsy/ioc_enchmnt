from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RESULT(Base):
    """
    Database model for results table.
    """

    __tablename__ = "result_table"

    id = Column(Integer, primary_key=True)
    ioc = Column(String(), nullable=False, unique=True)
    result = Column(JSON)
    info = Column(JSON)
