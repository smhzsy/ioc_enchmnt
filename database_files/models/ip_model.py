from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

IPBase = declarative_base()


class IP(IPBase):
    """
    Database model for IP table.
    """
    __tablename__ = "ip_table"

    id = Column(Integer, primary_key=True)
    ioc = Column(String(45), nullable=False, unique=True)
    alienvault = Column(String())
    brandefense_repo = Column(String())
    inquest = Column(String())
    threatfox = Column(String())
    whois = Column(String())
    virustotal = Column(String())
    location = Column(String())
    urlscan = Column(String())
    mg_db = Column(String())
    shodan = Column(String())
