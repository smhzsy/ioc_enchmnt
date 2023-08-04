import asyncio
import os

import shodan
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

sh_api_key = os.getenv("SHODAN_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def shodan_lookup_async(ip: str) -> None:
    """
    Searches for IP IoC in Shodan. Writes all data found to database.
    :param ip: IOC to search.
    :return: Info with logs.
    """
    session = create_session()
    try:
        api = shodan.Shodan(sh_api_key)

        host = api.host(ip)
        if "Access denied" in str(host):
            add_data(session, ip, "shodan", "IOC not found.", "ip_table")
            logger.info("Shodan info failed.")
        else:
            add_data(session, ip, "shodan", host, "ip_table")
            logger.info("Shodan info added.")
    except shodan.APIError as e:
        add_data(session, ip, "shodan", "Error occurred.", "ip_table")
        error_logger.error("Error occurred while trying to fetch data from Shodan: " + str(e))