from database_files.engine_creator import db_engine_create
from database_files.models.domain_model import DomainBase
from database_files.models.hash_model import HashBase
from database_files.models.ip_model import IPBase
from database_files.models.url_model import URLBase

engine = db_engine_create()


def create_tables():
    """
    Database method to create Database tables.
    """
    IPBase.metadata.create_all(engine)
    URLBase.metadata.create_all(engine)
    HashBase.metadata.create_all(engine)
    DomainBase.metadata.create_all(engine)
