import httpx

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def yara_hash_lookup_async(hash_value: str, result_list: list) -> None:
    """
    Searches for hash IOC in Yaraify. Writes all data found to database.
    :param result_list:
    :param hash_value: Hash IOC to search.
    :return: Info with logs.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "query": "lookup_hash",
        "search_term": hash_value,
    }
    session = create_session()

    async with httpx.AsyncClient() as client:
        try:
            api_url = "https://yaraify-api.abuse.ch/api/v1/"
            response = await client.post(api_url, json=data, headers=headers)
            response_data = response.json()

            if "no_results" in str(response_data):
                _.push(result_list, '"\'Yaraify\'":"False",')
                result_str = "".join(result_list)
                add_data(session, hash_value, result_str, "result")
                logger.info("Yaraify info failed.")
            else:
                _.push(result_list, '"\'Yaraify\'":"True",')
                result_str = "".join(result_list)
                add_data(session, hash_value, result_str, "result")
                logger.info("Yaraify info added.")
        except httpx.RequestError as e:
            _.push(result_list, '"\'Yaraify\'":"Error",')
            result_str = "".join(result_list)
            add_data(session, hash_value, result_str, "result")
            error_logger.error("Error occurred while trying to fetch data from Yaraify: " + str(e))
