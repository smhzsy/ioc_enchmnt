import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_ioc_threatfox_async(ioc: str, table_name: str) -> None:
    """
    Searches IOC in ThreatFox database. Adds all data to database.
    :param ioc: IOC to search for.
    :param table_name: The table name in database to add datas.
    :return: Info with logs.
    """
    url = 'https://threatfox-api.abuse.ch/api/v1/'
    headers = {'Content-Type': 'application/json'}
    data = {
        'query': 'search_ioc',
        'search_term': ioc
    }
    session = create_session()
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['query_status'] == 'ok':
                add_data(session, ioc, "threatfox", str(result['data']), table_name)
                logger.info("ThreatFox info added.")
            else:
                add_data(session, ioc, "threatfox", "IOC not found.", table_name)
                logger.info("ThreatFox info failed.")
        else:
            add_data(session, ioc, "threatfox", "Error occurred.", table_name)
            error_logger.error("Error while trying to fetch data from ThreatFox:" + str(response.status_code))
    except requests.exceptions.RequestException as e:
        add_data(session, ioc, "threatfox", "Error occurred.", table_name)
        error_logger.error("Error while trying to fetch data from ThreatFox:" + str(e))
