
from sqlalchemy.orm import sessionmaker

from database_files.engine_creator import db_engine_create
from database_files.models.hash_model import HASH

engine = db_engine_create()
Session = sessionmaker(bind=engine)
session = Session()


def get_hash_data(search_ioc: str) -> dict | None:
    """
    Takes all data and returns it from Hash table.
    :param search_ioc: The ioc to search for row.
    :return: Database data.
    """
    result = session.query(HASH).filter(HASH.ioc == search_ioc).first()

    if result is None:
        return None

    data = {
        'alienvault': result.alienvault,
        'brandefense_repo': result.brandefense_repo,
        'inquest': result.inquest,
        'threatfox': result.threatfox,
        'hybridanalysis': result.hybridanalysis,
        'virustotal': result.virustotal,
        'yaraify': result.yaraify
    }

    return data

