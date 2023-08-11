import os

import shodan
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _

load_dotenv()

sh_api_key = os.getenv("SHODAN_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def shodan_lookup_async(ip: str, result_list: list) -> None:
    """
    Searches for IP IoC in Shodan. Writes all data found to database.
    :param result_list:
    :param ip: IOC to search.
    :return: Info with logs.
    """
    session = create_session()
    try:
        api = shodan.Shodan(sh_api_key)

        host = await api.host(ip)
        if "Access denied" in str(host):
            _.push(result_list, "'Shodan': 'False'")
            result_str = "".join(result_list)
            add_data(session, ip, result_str, "result")
            logger.info("Shodan info failed.")
        else:
            _.push(result_list, "'Shodan': 'True'")
            result_str = "".join(result_list)
            add_data(session, ip, result_str, "result")
            logger.info("Shodan info added.")
    except shodan.APIError as e:
        _.push(result_list, "'Shodan': 'Error'")
        result_str = "".join(result_list)
        add_data(session, ip, result_str, "result")
        error_logger.error("Error occurred while trying to fetch data from Shodan: " + str(e))
