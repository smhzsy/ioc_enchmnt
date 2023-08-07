from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

HashBase = declarative_base()


class HASH(HashBase):
    """
    Database model for Hash table.
    """

    __tablename__ = "hash_table"

    id = Column(Integer, primary_key=True)
    ioc = Column(String(), nullable=False, unique=True)
    alienvault = Column(String())
    brandefense_repo = Column(String())
    inquest = Column(String())
    threatfox = Column(String())
    hybridanalysis = Column(String())
    virustotal = Column(String())
    yaraify = Column(String())
