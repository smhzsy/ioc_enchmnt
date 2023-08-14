from sqlalchemy.orm import sessionmaker

from database_files.engine_creator import db_engine_create
from database_files.model import RESULT

engine = db_engine_create()
Session = sessionmaker(bind=engine)
session = Session()


def get_data(search_ioc: str) -> dict | None:
    """
    Takes all data and returns it.
    :param search_ioc: The ioc to search for row.
    :return: Database data.
    """
    result = session.query(RESULT).filter(RESULT.ioc == search_ioc).first()

    if result is None:
        return None

    data = {
        "result": {result.result},
        "info": {result.info}
    }

    return data
