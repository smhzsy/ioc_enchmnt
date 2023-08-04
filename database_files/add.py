from sqlalchemy import create_engine

from database_files.models.domain_model import DomainBase
from database_files.models.hash_model import HashBase
from database_files.models.ip_model import IPBase
from database_files.models.url_model import URLBase
from database_files.session import create_session

engine = create_engine("postgresql://postgres:password@localhost/ioc_enchmnt")
IPBase.metadata.create_all(engine)
URLBase.metadata.create_all(engine)
HashBase.metadata.create_all(engine)
DomainBase.metadata.create_all(engine)


def add_data(session, ioc_value, column_name, value, table_name):
    table = None
    if table_name == "url_table":
        from database_files.models.url_model import URL

        table = URL
    elif table_name == "domain_table":
        from database_files.models.domain_model import DOMAIN

        table = DOMAIN
    elif table_name == "ip_table":
        from database_files.models.ip_model import IP

        table = IP
    elif table_name == "hash_table":
        from database_files.models.hash_model import HASH

        table = HASH

    if table is None:
        raise ValueError("Geçersiz tablo adı: {}".format(table_name))
    row = session.query(table).filter_by(ioc=ioc_value).first()
    if row:
        setattr(row, column_name, value)
    else:
        new_row = table(ioc=ioc_value, **{column_name: value})
        session.add(new_row)

    session.commit()


session = create_session()
add_data(session, "test url", "inquest", "success", "domain_table")
