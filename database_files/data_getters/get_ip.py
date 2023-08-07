from typing import Any

from sqlalchemy.orm import sessionmaker

from database_files.engine_creator import db_engine_create
from database_files.models.ip_model import IP

engine = db_engine_create()
Session = sessionmaker(bind=engine)
session = Session()


def get_ip_data(search_ioc: str) -> dict | None:
    """
    Takes all data and returns it from IP table.
    :param search_ioc: The ioc to search for row.
    :return: Database data.
    """
    result = session.query(IP).filter(IP.ioc == search_ioc).first()

    if result is None:
        return None

    data = {
        'alienvault': result.alienvault,
        'brandefense_repo': result.brandefense_repo,
        'inquest': result.inquest,
        'threatfox': result.threatfox,
        'whois': result.whois,
        'virustotal': result.virustotal,
        'location': result.location,
        'urlscan': result.urlscan,
        'mg_db': result.mg_db,
        'shodan': result.shodan
    }

    return data
