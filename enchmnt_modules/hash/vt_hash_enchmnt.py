import asyncio
import os

import requests
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_virustotal_hash_info_async(hash_value: str) -> None:
    """
    Searches for hash IOC in VirusTotal. Writes all data found to database.
    :param hash_value: Hash IOC to search
    :return: Info with logs.
    """
    url = f"https://www.virustotal.com/api/v3/files/{hash_value}"

    headers = {"accept": "application/json", "x-apikey": vt_api_key}
    session = create_session()
    try:
        response = requests.get(url, headers=headers)
        if response:
            add_data(session, hash_value, "virustotal", response.text, "hash_table")
            logger.info("VirusTotal Hash info added.")
        else:
            add_data(session, hash_value, "virustotal", "IOC not found.", "hash_table")
            logger.info("VirusTotal Hash info failed.")
    except Exception as e:
        add_data(session, hash_value, "virustotal", "Error occurred.", "hash_table")
        error_logger.error(
            "Error occurred while trying to fetch data from VirusTotal Hash: " + str(e)
        )
