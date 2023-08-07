from sqlalchemy.orm import sessionmaker

from database_files.engine_creator import db_engine_create
from database_files.models.domain_model import DOMAIN

engine = db_engine_create()
Session = sessionmaker(bind=engine)
session = Session()


def get_domain_data(search_ioc: str) -> dict | None:
    """
    Takes all data and returns it from Domain table.
    :param search_ioc: The ioc to search for row.
    :return: Database data.
    """
    result = session.query(DOMAIN).filter(DOMAIN.ioc == search_ioc).first()

    if result is None:
        return None

    data = {
        "alienvault": result.alienvault,
        "brandefense_repo": result.brandefense_repo,
        "inquest": result.inquest,
        "threatfox": result.threatfox,
        "whois": result.whois,
        "urlscan": result.urlscan,
        "location": result.location,
        "virustotal": result.virustotal,
        "mg_db": result.mg_db,
    }

    return data
