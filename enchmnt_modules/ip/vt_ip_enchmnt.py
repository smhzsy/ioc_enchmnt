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


async def get_virustotal_ip_info_async(ip: str) -> None:
    """
    Searches for IP IoC in VirusTotal. Writes all data found to database.
    :param ip: IOC to search.
    :return: Info with logs.
    """
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    headers = {
        "accept": "application/json",
        "x-apikey": vt_api_key
    }
    session = create_session()
    try:
        response = requests.get(url, headers=headers)
        if response:
            add_data(session, ip, "virustotal", response.text, "ip_table")
            logger.info("VirusTotal IP info added.")
        else:
            add_data(session, ip, "virustotal", "IOC not found.", "ip_table")
            logger.info("VirusTotal IP info failed.")
    except Exception as e:
        add_data(session, ip, "virustotal", "Error occurred.", "ip_table")
        error_logger.error("Error occurred while trying to fetch data from VirusTotal IP: " + str(e))
