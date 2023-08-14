import httpx

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def mg_domain_lookup_async(input_value: str, result_list: list) -> None:
    """
    Searches IOC in Mertcan Gokgoz's bad domain's list.
    :param result_list:
    :param input_value: The IOC to search
    :return: Info with logs.
    """
    url = "https://raw.githubusercontent.com/mertcangokgoz/public-disavow-links/main/disavow-links.txt"
    session = create_session()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            domains = response.text.splitlines()
            found = False

            for domain in domains:
                if input_value.lower() in domain.lower():
                    _.push(result_list, '"\'Mertcan Gokgoz\'":"True",')
                    result_str = "".join(result_list)
                    add_data(session, input_value, result_str, "result")
                    logger.info("Mertcan Gokgoz domain info added.")
                    found = True

            if not found:
                _.push(result_list, '"\'Mertcan Gokgoz\'":"False",')
                result_str = "".join(result_list)
                add_data(session, input_value, result_str, "result")
                logger.info("Mertcan Gokgoz domain info failed.")

        except httpx.RequestError as e:
            _.push(result_list, '"\'Mertcan Gokgoz\'":"Error",')
            result_str = "".join(result_list)
            add_data(session, input_value, result_str, "result")
            error_logger.error("Error occurred while trying to fetch data from MG domain: " + str(e))
