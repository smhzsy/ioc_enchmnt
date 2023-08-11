import httpx
import pydash as _

import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_iq_info_async(keyword: str, result_list: list) -> None:
    """
    Getting all the datas from InQuest.
    :param result_list: The results list.
    :param keyword: IOC to search.
    :return: Info with logs.
    """
    url = f"https://labs.inquest.net/api/iocdb/search?keyword={keyword}&filter_by="

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        session = create_session()
        if response.status_code == 200:
            response_dict = response.json()
            if response_dict["data"]:
                _.push(result_list, "'InQuest': 'True'")
                result_str = "".join(result_list)
                add_data(session, keyword, result_str, "result")
                logger.info("InQuest info added.")
            else:
                _.push(result_list, "'InQuest': 'False'")
                result_str = "".join(result_list)
                add_data(session, keyword, result_str, "result")
                logger.info("InQuest info failed.")
        else:
            _.push(result_list, "'InQuest': 'Error'")
            result_str = "".join(result_list)
            add_data(session, keyword, result_str, "result")
            error_logger.error("Error in InQuest.")
