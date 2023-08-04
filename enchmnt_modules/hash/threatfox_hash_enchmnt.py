import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_hash_threatfox_async(file_hash: str) -> None:
    """
    Searches for IOC in ThreatFox hash database. Writes all data found to database.
    :param file_hash: IOC to search.
    :return: Info with logs.
    """
    url = 'https://threatfox-api.abuse.ch/api/v1/'
    headers = {'Content-Type': 'application/json'}
    data = {
        'query': 'search_hash',
        'hash': file_hash
    }
    session = create_session()
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['query_status'] == 'ok':
                add_data(session, file_hash, "threatfox", str(result['data']), "hash_table")
                logger.info("ThreatFox Hash info added.")
            else:
                add_data(session, file_hash, "threatfox", "IOC not found.", "hash_table")
                logger.info("ThreatFox Hash info failed.")
        else:
            add_data(session, file_hash, "threatfox", "Error occurred.", "hash_table")
            error_logger.error("Error occurred while trying to fetch data from ThreatFox hash database: " + str(response.status_code))
    except requests.exceptions.RequestException as e:
        add_data(session, file_hash, "threatfox", "Error occurred.", "hash_table")
        error_logger.error("Error occurred while trying to fetch data from ThreatFox hash database: " + str(e))

