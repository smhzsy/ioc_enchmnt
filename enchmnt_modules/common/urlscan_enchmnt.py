import httpx

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
from enums import InputType

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_urlscan_info_async(type: InputType, keyword: str, result_list: list) -> None:
    """
    Searches the ioc in UrlScan. Adds all data to database.
    :param result_list:
    :param type: IOC type for API request.
    :param keyword: The IOC to search.
    :return: Info with logs.
    """
    indicator_type_dict = {
        InputType.DOMAIN: "domain",
        InputType.IP: "ip",
    }
    indicator_type = indicator_type_dict.get(type)
    url = f"https://urlscan.io/api/v1/search/?q={indicator_type}:{keyword}"
    session = create_session()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response_dict = response.json()

            if response_dict["results"]:
                _.push(result_list, '"\'UrlScan\'":"True",')
                result_str = "".join(result_list)
                add_data(session, keyword, result_str, "result")
                logger.info("UrlScan info added.")
            else:
                _.push(result_list, '"\'UrlScan\'":"False",')
                result_str = "".join(result_list)
                add_data(session, keyword, result_str, "result")
                logger.info("UrlScan info failed.")
        except httpx.RequestError as e:
            _.push(result_list, '"\'UrlScan\'":"Error",')
            result_str = "".join(result_list)
            add_data(session, keyword, result_str, "result")
            error_logger.error("Error occurred while trying to fetch data from UrlScan: " + str(e))

