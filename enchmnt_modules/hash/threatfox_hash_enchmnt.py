import httpx

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_hash_threatfox_async(file_hash: str, result_list: list) -> None:
    """
    Searches for IOC in ThreatFox hash database. Writes all data found to database.
    :param result_list:
    :param file_hash: IOC to search.
    :return: Info with logs.
    """
    url = "https://threatfox-api.abuse.ch/api/v1/"
    headers = {"Content-Type": "application/json"}
    data = {"query": "search_hash", "hash": file_hash}
    session = create_session()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            result = response.json()

            if response.status_code == 200 and result["query_status"] == "ok":
                _.push(result_list, '"\'ThreatFox\'":"True",')
                result_str = "".join(result_list)
                add_data(session, file_hash, result_str, "result")
                logger.info("ThreatFox Hash info added.")
            else:
                _.push(result_list, '"\'ThreatFox\'":"False",')
                result_str = "".join(result_list)
                add_data(session, file_hash, result_str, "result")
                logger.info("ThreatFox Hash info failed.")
        except httpx.RequestError as e:
            _.push(result_list, '"\'ThreatFox\'":"Error",')
            result_str = "".join(result_list)
            add_data(session, file_hash, result_str, "result")
            error_logger.error("Error occurred while trying to fetch data from ThreatFox hash database: " + str(e))

