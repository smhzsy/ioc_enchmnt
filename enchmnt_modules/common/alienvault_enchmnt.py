import os
import httpx
import pydash as _
from dotenv import load_dotenv
from enums import InputType
from database_files.add import add_data
from database_files.session import create_session
import logger_config

load_dotenv()

av_api_key = os.getenv("ALIENVAULT_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_indicator_in_alienvault_async(type: InputType, indicator_value: str, result_list: list) -> None:
    """
    Scans the ioc in alienvault's database. Adds all to info found to database.
    :param type: Type of IoC.
    :param result_list: The Result String.
    :param indicator_value: The ioc to search.
    :return: Info with logs.
    """
    indicator_type_dict = {
        InputType.URL: "url",
        InputType.DOMAIN: "domain",
        InputType.MD5_HASH: "file",
        InputType.SHA1_HASH: "file",
        InputType.SHA256_HASH: "file",
        InputType.IP: "IPv4",
    }
    indicator_type = indicator_type_dict.get(type)
    endpoint = f"https://otx.alienvault.com/api/v1/indicators/{indicator_type}/{indicator_value}/general"
    headers = {"X-OTX-API-KEY": av_api_key}
    session = create_session()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()

            if response.status_code == 200:
                _.push(result_list, '"\'AlienVault\'":"True",')
                result_str = "".join(result_list)
                add_data(session, indicator_value, result_str, "result")
                logger.info("AlienVault info added.")
            else:
                _.push(result_list, '"\'AlienVault\'":"False",')
                result_str = "".join(result_list)
                add_data(session, indicator_value, result_str, "result")
                error_logger.error("Error: Unable to find data in AlienVault")

    except httpx.HTTPError as e:
        _.push(result_list, '"\'AlienVault\'":"Error",')
        result_str = "".join(result_list)
        add_data(session, indicator_value, result_str, "result")
        error_logger.error("AlienVault Client Error: %s", e)
