import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def yara_hash_lookup_async(hash_value: str) -> None:
    """
    Searches for hash IOC in Yaraify. Writes all data found to database.
    :param hash_value: Hash IOC to search.
    :return: Info with logs.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "query": "lookup_hash",
        "search_term": hash_value,
    }
    session = create_session()
    try:
        api_url = "https://yaraify-api.abuse.ch/api/v1/"
        response = requests.post(api_url, json=data, headers=headers)
        response_data = response.json()
        if "no_results" in str(response_data):
            add_data(session, hash_value, "yaraify", "IOC not found.", "hash_table")
            logger.info("Yaraify info failed.")
        else:
            add_data(session, hash_value, "yaraify", str(response_data), "hash_table")
            logger.info("Yaraify info added.")
    except requests.RequestException as e:
        add_data(session, hash_value, "yaraify", "Error occurred.", "hash_table")
        error_logger.error(
            "Error occurred while trying to fetch data from Yaraify: " + str(e)
        )
