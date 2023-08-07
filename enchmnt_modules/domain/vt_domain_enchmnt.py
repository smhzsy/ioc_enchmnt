import os

import requests
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_virustotal_domain_info_async(domain: str) -> None:
    """
    Searches IOC domain in VirusTotal. Writes all data found to database.
    :param domain: The IOC to search.
    :return: Info with logs.
    """
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    headers = {"accept": "application/json", "x-apikey": vt_api_key}

    response = requests.get(url, headers=headers)
    session = create_session()
    try:
        if response:
            add_data(session, domain, "virustotal", response.text, "domain_table")
            logger.info("VirusTotal domain info added.")
        else:
            add_data(session, domain, "virustotal", "IOC not found.", "domain_table")
            logger.info("VirusTotal domain info failed.")
    except Exception as e:
        add_data(session, domain, "virustotal", "Error occurred.", "domain_table")
        error_logger.error(
            "Error occured while trying to fetch data from VirusTotal domain: " + str(e)
        )
