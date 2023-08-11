from sqlalchemy.orm import Session

from database_files.engine_creator import db_engine_create

engine = db_engine_create()

from database_files.model import RESULT


def add_data(session: Session, ioc_value: str, value: str, column: str) -> None:
    """
    Database method for writing datas found to database.
    :param column:
    :param session: Database session.
    :param ioc_value: Unique key.
    :param value: The data.
    :return: None
    """
    table = RESULT

    row = session.query(table).filter_by(ioc=ioc_value).first()
    if row:
        setattr(row, f"{column}", value)
    else:
        new_row = table(ioc=ioc_value, **{f"{column}": value})
        session.add(new_row)

    session.commit()
    session.close()
