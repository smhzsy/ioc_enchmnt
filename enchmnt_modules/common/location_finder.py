import requests

import logging

from database_files.add import add_data
from database_files.session import create_session

logger = logging.getLogger(__name__)


async def get_location_async(keyword: str, table_name: str):
    logger.info("Starting search with ioc: %s", keyword)
    url = f"http://ip-api.com/json/{keyword}"
    response = requests.request("GET", url)
    if response:
        logger.info("Finished search with result: %s", response.text)
    session = create_session()
    add_data(session, keyword, "location", response.text, table_name)


