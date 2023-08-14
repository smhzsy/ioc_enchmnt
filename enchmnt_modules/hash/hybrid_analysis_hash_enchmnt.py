import os

import httpx
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
load_dotenv()

hyan_api_key = os.getenv("HYBRID_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_hyan_hash_info_async(hash_to_look: str, result_list: list) -> None:
    """
    Searches for IOC in HybridAnalysis database. Writes all data found to database.
    :param result_list:
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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, data=data)
            json_response = str(response.json())

            if json_response:
                if "validation_errors" in json_response:
                    _.push(result_list,'"\'HybridAnalysis\'":"False",')
                    result_str = "".join(result_list)
                    add_data(session, hash_to_look, result_str, "result")
                    logger.info("HybridAnalysis info failed.")
                else:
                    _.push(result_list, '"\'HybridAnalysis\'":"True",')
                    result_str = "".join(result_list)
                    add_data(session, hash_to_look, result_str, "result")
                    logger.info("HybridAnalysis info added.")
        except httpx.RequestError as e:
            _.push(result_list, '"\'HybridAnalysis\'":"Error",')
            result_str = "".join(result_list)
            add_data(session, hash_to_look, result_str, "result")
            error_logger.error("Error occurred while trying to fetch data from HybridAnalysis: " + str(e))
