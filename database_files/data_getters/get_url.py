
from sqlalchemy.orm import sessionmaker

from database_files.engine_creator import db_engine_create
from database_files.models.url_model import URL

engine = db_engine_create()
Session = sessionmaker(bind=engine)
session = Session()


def get_url_data(search_ioc: str) -> dict | None:
    """
    Takes all data and returns it from IP table.
    :param search_ioc: The ioc to search for row.
    :return: Database data.
    """
    result = session.query(URL).filter(URL.ioc == search_ioc).first()

    if result is None:
        return None

    data = {
        'alienvault': result.alienvault,
        'brandefense_repo': result.brandefense_repo,
        'inquest': result.inquest,
        'threatfox': result.threatfox,
        'apivoid': result.apivoid,
        'whois': result.whois,
        'location': result.location,
        'virustotal': result.virustotal
    }

    return data

