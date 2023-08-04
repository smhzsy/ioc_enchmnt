import asyncio
import json
import os

import requests
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

hyan_api_key = os.getenv("HYBRID_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_hyan_hash_info_async(hash_to_look: str) -> None:
    """
    Searches for IOC in HybridAnalysis database. Writes all data found to database.
    :param hash_to_look: IOC to search.
    :return: Info with logs.
    """
    url = "https://www.hybrid-analysis.com/api/v2/search/hash"
    headers = {
        "accept": "application/json",
        "user-agent": "Falcon Sandbox",
        "api-key": hyan_api_key,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"hash": hash_to_look}
    session = create_session()
    try:
        response = requests.post(url, headers=headers, data=data)
        json_response = str(response.json())
        if json_response:
            if "validation_errors" in json_response:
                add_data(
                    session,
                    hash_to_look,
                    "hybridanalysis",
                    "IOC not found.",
                    "hash_table",
                )
                logger.info("HybridAnalysis info failed.")
            else:
                add_data(
                    session, hash_to_look, "hybridanalysis", json_response, "hash_table"
                )
                logger.info("HybridAnalysis info added.")
    except Exception as e:
        add_data(
            session, hash_to_look, "hybridanalysis", "Error occurred.", "hash_table"
        )
        error_logger.error(
            "Error occurred while trying to fetch data from HybridAnalysis: " + str(e)
        )
