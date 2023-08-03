import os

import requests
from dotenv import load_dotenv

from celery_files.celery_config import app

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")




@app.task
def get_virustotal_domain_info_async(domain: str):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    headers = {
        "accept": "application/json",
        "x-apikey": vt_api_key
    }

    response = requests.get(url, headers=headers)

    print(response.text)
