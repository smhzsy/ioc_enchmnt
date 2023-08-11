import os

import httpx
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
load_dotenv()

apivoid_api_key = os.getenv("APIVOID_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_apivoid_url_async(url: str, result_list: list) -> None:
    """
    Searches for IP IoC in ApiVoid. Writes all data found to database.
    :param result_list:
    :param url: IOC to search.
    :return: Info with logs.
    """
    api_endpoint = "https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/"
    params = {"key": apivoid_api_key, "url": url}
    session = create_session()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_endpoint, params=params)

            if response.status_code == 200:
                _.push(result_list, "'UrlVoid': 'True'")
                result_str = "".join(result_list)
                add_data(session, url, result_str, "result")
                logger.info("ApiVoid info added.")
            else:
                _.push(result_list, "'UrlVoid': 'False'")
                result_str = "".join(result_list)
                add_data(session, url, result_str, "result")
                logger.info("ApiVoid info failed.")
        except httpx.RequestError as e:
            _.push(result_list, "'UrlVoid': 'Error'")
            result_str = "".join(result_list)
            add_data(session, url, result_str, "result")
            error_logger.error("Error occurred while trying to fetch data from ApiVoid: " + str(e))
