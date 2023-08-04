from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DomainBase = declarative_base()


class DOMAIN(DomainBase):
    __tablename__ = "domain_table"

    id = Column(Integer, primary_key=True)
    ioc = Column(String(), nullable=False, unique=True)
    alienvault = Column(String())
    brandefense_repo = Column(String())
    inquest = Column(String())
    threatfox = Column(String())
    whois = Column(String())
    urlscan = Column(String())
    location = Column(String())
    virustotal = Column(String())
    mg_db = Column(String())
