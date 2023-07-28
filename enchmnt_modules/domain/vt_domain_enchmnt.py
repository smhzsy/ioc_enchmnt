import os

import requests
from dotenv import load_dotenv

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")


def get_virustotal_domain_info(domain: str):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    headers = {
        "accept": "application/json",
        "x-apikey": vt_api_key
    }

    response = requests.get(url, headers=headers)

    print(response.text)
