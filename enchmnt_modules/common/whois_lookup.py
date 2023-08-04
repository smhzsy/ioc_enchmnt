
import json

import whois

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def whois_lookup_async(input_ioc: str, table_name: str) -> None:
    """
    Gets the whois info of the IOC. Writes all data to database.
    :param input_ioc: IOC to search.
    :param table_name: The table name in database to add datas.
    :return: Info with logs.
    """
    session = create_session()
    try:
        w = whois.whois(input_ioc)
        response_dict = json.loads(str(w))
        if response_dict["domain_name"] is not None:
            add_data(session, input_ioc, "whois", str(w), table_name)
            logger.info("Whois info added.")
        else:
            add_data(session, input_ioc, "whois","IOC not found.", table_name)
            logger.info("Whois info failed.")
    except Exception as e:
        add_data(session, input_ioc, "whois", "Error occurred.", table_name)
        error_logger.error("Error while trying to fetch data from whois: " + str(e))


