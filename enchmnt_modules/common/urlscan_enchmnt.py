import asyncio
import json

import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_urlscan_info_async(type: str, keyword: str, table_name: str) -> None:
    """
    Searches the ioc in UrlScan. Adds all data to database.
    :param type: IOC type for API request.
    :param keyword: The IOC to search.
    :param table_name: The table name in database to add datas.
    :return: Info with logs.
    """
    url = f"https://urlscan.io/api/v1/search/?q={type}:{keyword}"
    response = requests.request("GET", url)
    session = create_session()
    response_dict = json.loads(response.text)
    try:
        if response_dict["results"]:
            add_data(
                session, keyword, "urlscan", str(response_dict["results"]), table_name
            )
            logger.info("UrlScan info added.")
        else:
            add_data(session, keyword, "urlscan", "IOC not found.", table_name)
            logger.info("UrlScan info failed.")
    except Exception as e:
        add_data(session, keyword, "urlscan", "Error occurred.", table_name)
        error_logger.error(
            "Error occurred while trying to fetch data from UrlScan: " + str(e)
        )
