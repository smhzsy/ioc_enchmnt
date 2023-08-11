import json

import whois

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def whois_lookup_async(input_ioc: str, info_list: list) -> None:
    """
    Gets the whois info of the IOC. Writes all data to database.
    :param info_list: The list for extra info.
    :param input_ioc: IOC to search.
    :return: Info with logs.
    """
    session = create_session()
    try:
        w = whois.whois(input_ioc)
        response_dict = json.loads(str(w))
        if response_dict["domain_name"] is not None:
            domain = response_dict["domain_name"]
            regin = response_dict["registrant_name"]
            regis = response_dict["registrar"]
            update = response_dict["updated_date"]
            exp = response_dict["expiration_date"]
            _.push(info_list, f"'Domain': '{domain}'")
            _.push(info_list, f"'Registrant Name': '{regin}'")
            _.push(info_list, f"'Registrar': '{regis}'")
            _.push(info_list, f"'Updated Date': '{update}'")
            _.push(info_list, f"'Expiration Date': '{exp}'")

            result_str = "".join(info_list)
            add_data(session, input_ioc, result_str, "info")
            logger.info("Whois info added.")
        else:
            _.push(info_list, "'WhoIs': 'Not Found.'")
            result_str = "".join(info_list)
            add_data(session, input_ioc, result_str, "info")
            logger.info("Whois info failed.")
    except Exception as e:
        _.push(info_list, "'WhoIs': 'Error.'")
        result_str = "".join(info_list)
        add_data(session, input_ioc, result_str, "info")
        error_logger.error("Error while trying to fetch data from whois: " + str(e))
