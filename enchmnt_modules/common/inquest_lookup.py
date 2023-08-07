import json

import requests

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_iq_info_async(keyword: str, table_name: str) -> None:
    """
    Getting all the datas from InQuest.
    :param keyword: IOC to search
    :param table_name: The table name in database to add datas.
    :return: Info with logs.
    """
    url = f"https://labs.inquest.net/api/iocdb/search?keyword={keyword}&filter_by="
    response = requests.request("GET", url)
    session = create_session()
    if response:
        response_dict = json.loads(response.text)
        if response_dict["data"]:
            add_data(
                session, keyword, "inquest", str(response_dict["data"]), table_name
            )
            logger.info("InQuest info added.")
        else:
            add_data(session, keyword, "inquest", "IOC not found.", table_name)
    else:
        add_data(session, keyword, "inquest", "Error occurred.", table_name)
        error_logger.error("Error")
