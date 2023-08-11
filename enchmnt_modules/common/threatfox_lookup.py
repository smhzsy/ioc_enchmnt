import httpx

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_ioc_threatfox_async(ioc: str, result_list: list) -> None:
    """
    Searches IOC in ThreatFox database. Adds all data to database.
    :param result_list: The result list.
    :param ioc: IOC to search for.
    :return: Info with logs.
    """
    url = "https://threatfox-api.abuse.ch/api/v1/"
    headers = {"Content-Type": "application/json"}
    data = {"query": "search_ioc", "search_term": ioc}
    session = create_session()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                if result["query_status"] == "ok":
                    _.push(result_list, "'ThreatFox': 'True'")
                    result_str = "".join(result_list)
                    add_data(session, ioc, result_str, "result")
                    logger.info("ThreatFox info added.")
                else:
                    _.push(result_list, "'ThreatFox': 'False'")
                    result_str = "".join(result_list)
                    add_data(session, ioc, result_str, "result")
                    logger.info("ThreatFox info failed.")
            else:
                _.push(result_list, "'ThreatFox': 'Error'")
                result_str = "".join(result_list)
                add_data(session, ioc, result_str, "result")
                error_logger.error(
                    "Error while trying to fetch data from ThreatFox:"
                    + str(response.status_code)
                )
        except httpx.RequestError as e:
            _.push(result_list, "'ThreatFox': 'Error'")
            result_str = "".join(result_list)
            add_data(session, ioc, result_str, "result")
            error_logger.error("Error while trying to fetch data from ThreatFox:" + str(e))

