import os

import aiohttp
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

av_api_key = os.getenv("ALIENVAULT_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_indicator_in_alienvault_async(indicator_type: str, indicator_value: str, table_name: str) -> None:
    """
    Scans the ioc in alienvault's database. Adds all to info found to database.
    :param indicator_type: Special type of the ioc which is specified by AlienVault.
    :param indicator_value: The ioc to search.
    :param table_name: The name of the table which the data will be written.
    :return: Info with logs.
    """
    endpoint = f"https://otx.alienvault.com/api/v1/indicators/{indicator_type}/{indicator_value}/general"
    headers = {"X-OTX-API-KEY": av_api_key}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                response_data = await response.json()

                if response.status == 200:
                    session = create_session()
                    add_data(session, indicator_value, "alienvault", str(response_data), table_name)
                    logger.info("AlienVault info added.")
                else:
                    add_data(session, indicator_value, "alienvault", "IOC not found.", table_name)
                    error_logger.error("Error: Unable to find data in AlienVault")

    except aiohttp.ClientError as e:
        add_data(session, indicator_value, "alienvault", "Error occurred.", table_name)
        error_logger.error("AlienVault Client Error: ", e)
