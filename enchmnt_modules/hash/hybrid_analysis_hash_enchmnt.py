import os

import requests
from dotenv import load_dotenv

from celery_files.celery_config import app

load_dotenv()

hyan_api_key = os.getenv("HYBRID_API_KEY")




@app.task
def get_hyan_hash_info_async(hash_to_look: str):
    url = 'https://www.hybrid-analysis.com/api/v2/search/hash'
    headers = {
        'accept': 'application/json',
        'user-agent': 'Falcon Sandbox',
        'api-key': hyan_api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'hash': hash_to_look
    }

    response = requests.post(url, headers=headers, data=data)

    json_response = response.json()

    print(json_response)

