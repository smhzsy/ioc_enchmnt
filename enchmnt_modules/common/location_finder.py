import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_location_async(keyword: str, table_name: str) -> None:
    """
    Getting the geometric location of ioc.
    :param keyword: Ioc to search
    :param table_name: The database table which the code will add the data.
    :return: Info with logs
    """
    url = f"http://ip-api.com/json/{keyword}"
    response = requests.request("GET", url)
    session = create_session()
    try:
        if response:
            add_data(session, keyword, "location", response.text, table_name)
            logger.info("Location info added.")
        else:
            add_data(session, keyword, "location", "Couldn't find location.", table_name)
            logger.info("Location info failed.")
    except Exception as e:
        add_data(session, keyword, "location", "Error occurred.", table_name)
        error_logger.error("Error while trying to get Location Info: %s", str(e))
