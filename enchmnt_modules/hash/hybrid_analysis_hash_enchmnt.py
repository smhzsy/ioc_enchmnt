import os

import requests
from dotenv import load_dotenv

from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

hyan_api_key = os.getenv("HYBRID_API_KEY")



async def get_hyan_hash_info_async(hash_to_look: str):
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
    if json_response:
        session = create_session()
        add_data(session, hash_to_look, "hybridanalysis", str(json_response), "hash_table")

