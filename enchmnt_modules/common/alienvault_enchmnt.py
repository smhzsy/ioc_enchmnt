import os

import requests
from dotenv import load_dotenv

from celery_files.celery_config import app

load_dotenv()

av_api_key = os.getenv("ALIENVAULT_API_KEY")




@app.task
def search_indicator_in_alienvault_async(indicator_type, indicator_value):
    endpoint = f"https://otx.alienvault.com/api/v1/indicators/{indicator_type}/{indicator_value}/general"
    headers = {"X-OTX-API-KEY": av_api_key}

    try:
        response = requests.get(endpoint, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            print("success")
            return response_data

        else:
            print("Error: Unable to fetch data from AlienVault.")
            return None

    except requests.exceptions.RequestException as e:
        print("Error: Request Exception -", e)
        return None
