import os

import requests
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

apivoid_api_key = os.getenv("APIVOID_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_apivoid_url_async(url: str) -> None:
    """
    Searches for IP IoC in ApiVoid. Writes all data found to database.
    :param url: IOC to search.
    :return: Info with logs.
    """
    api_endpoint = "https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/"
    params = {
        'key': apivoid_api_key,
        'url': url
    }
    session = create_session()
    try:
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            result = response.json()
            add_data(session, url, "apivoid", str(result), "url_table")
            logger.info("ApiVoid info added.")
        else:
            add_data(session, url, "apivoid", "IOC not found.", "url_table")
            logger.info("ApiVoid info failed.")
    except requests.exceptions.RequestException as e:
        add_data(session, url, "apivoid", "Error occurred.", "url_table")
        error_logger.error("Error occurred while trying to fetch data from ApiVoid: " + str(e))
