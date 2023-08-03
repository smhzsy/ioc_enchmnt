import requests

from celery_files.celery_config import app
import logging

logger = logging.getLogger(__name__)

@app.task
def get_location_async(keyword: str):
    logger.info("Starting search with ioc: %s", keyword)
    url = f"http://ip-api.com/json/{keyword}"
    response = requests.request("GET", url)
    if response:
        logger.info("Finished search with result: %s", response.text)
    print(response.text)


