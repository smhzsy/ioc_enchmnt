import os

import httpx
import pydash as _
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session
from enums import InputType

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_virustotal_info_async(type: InputType, ioc: str, result_list: list) -> None:
    """
    Searches for hash IOC in VirusTotal. Writes all data found to database.
    :param type:
    :param result_list:
    :param ioc:
    :return: Info with logs.
    """
    indicator_type_dict = {
        InputType.DOMAIN: "domains",
        InputType.MD5_HASH: "files",
        InputType.SHA1_HASH: "files",
        InputType.SHA256_HASH: "files",
        InputType.IP: "ip_addresses",
    }
    indicator_type = indicator_type_dict.get(type)
    url = f"https://www.virustotal.com/api/v3/{indicator_type}/{ioc}"

    headers = {"accept": "application/json", "x-apikey": vt_api_key}
    session = create_session()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                _.push(result_list, "'VirusTotal': 'True'")
                result_str = "".join(result_list)
                add_data(session, ioc, result_str, "result")
                logger.info("VirusTotal Hash info added.")
            else:
                _.push(result_list, "'VirusTotal': 'False'")
                result_str = "".join(result_list)
                add_data(session, ioc, result_str, "result")
                logger.info("VirusTotal Hash info failed.")
        except Exception as e:
            _.push(result_list, "'VirusTotal': 'Error'")
            result_str = "".join(result_list)
            add_data(session, ioc, result_str, "result")
            error_logger.error(
                "Error occurred while trying to fetch data from VirusTotal Hash: " + str(e)
            )
