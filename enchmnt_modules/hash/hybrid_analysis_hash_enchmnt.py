import os

import requests
from dotenv import load_dotenv

load_dotenv()

hyan_api_key = os.getenv("HYBRID_API_KEY")


def get_hyan_hash_info(hash_to_look: str):
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


get_hyan_hash_info("8ffbb7a80efa9ee79e996abde7a95cf8dc6f9a41f9026672a8dbd95539fea82a")
