from sqlalchemy.orm import Session

from database_files.engine_creator import db_engine_create

engine = db_engine_create()


def add_data(
    session: Session, ioc_value: str, column_name: str, value: str, table_name: str
) -> None:
    """
    Database method for writing datas found to database.
    :param session: Database session.
    :param ioc_value: Unique key.
    :param column_name: The column which data will be written.
    :param value: The data.
    :param table_name: The table name to write data.
    :return: None
    """
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
