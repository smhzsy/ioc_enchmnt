import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def mg_domain_lookup_async(input_value: str) -> None:
    """
    Searches IOC in Mertcan Gokgoz's bad domain's list.
    :param input_value: The IOC to search
    :return: Info with logs.
    """
    url = "https://raw.githubusercontent.com/mertcangokgoz/public-disavow-links/main/disavow-links.txt"
    session = create_session()
    try:
        response = requests.get(url)
        response.raise_for_status()
        domains = response.text.splitlines()
        for domain in domains:
            if input_value.lower() in domain.lower():
                add_data(session, input_value, "mg_db", "IOC Found in Repo.", "domain_table")
                logger.info("Mertcan Gokgoz domain info added.")
        else:
            add_data(session, input_value, "mg_db", "IOC not found.", "domain_table")
            logger.info("Mertcan Gokgoz domain info failed.")
    except requests.exceptions.RequestException as e:
        add_data(session, input_value, "mg_db", "Error occurred.", "domain_table")
        error_logger.error("Error occurred while trying to fetch data from MG domain: " + str(e))
