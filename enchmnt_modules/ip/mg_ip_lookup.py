import asyncio

import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def mg_ip_lookup_async(ip_address: str) -> None:
    """
    Searches IP IoC in Mertcan Gokgoz bad IP database. Writes all data found to database.
    :param ip_address:
    :return:
    """
    session = create_session()
    try:
        url = f"https://check.mertcan.dev/check.php?ip={ip_address}"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        if "false" in str(json_data):
            add_data(session, ip_address, "mg_db", "IOC not found.", "ip_table")
            logger.info("Mertcan Gokgoz ip info failed.")
        elif "invalid query" in str(json_data):
            add_data(session, ip_address, "mg_db", "IOC type error.", "ip_table")
            logger.info("Mertcan Gokgoz ip info failed. (type error)")
        else:
            add_data(session, ip_address, "mg_db", str(json_data), "ip_table")
            logger.info("Mertcan Gokgoz ip info added.")
    except Exception as e:
        add_data(session, ip_address, "mg_db", "Error occurred.", "ip_table")
        error_logger.error(
            "Error occurred while trying to fetch data from MG bad IP API: " + str(e)
        )
