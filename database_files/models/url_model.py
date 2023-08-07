from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

URLBase = declarative_base()


class URL(URLBase):
    """
    Database model for URL table.
    """
    __tablename__ = "url_table"

    id = Column(Integer, primary_key=True)
    ioc = Column(String(), nullable=False, unique=True)
    alienvault = Column(String())
    brandefense_repo = Column(String())
    inquest = Column(String())
    threatfox = Column(String())
    apivoid = Column(String())
    whois = Column(String())
    location = Column(String())
    virustotal = Column(String())
