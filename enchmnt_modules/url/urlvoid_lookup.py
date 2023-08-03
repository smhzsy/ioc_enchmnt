import os

import requests
from dotenv import load_dotenv

load_dotenv()

apivoid_api_key = os.getenv("APIVOID_API_KEY")

from celery_files.celery_config import app


@app.task
def search_apivoid_url_async(url):
    api_endpoint = "https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/"
    params = {
        'key': apivoid_api_key,
        'url': url
    }

    try:
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

    return None
