import os

import requests
from dotenv import load_dotenv

from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")


async def get_virustotal_domain_info_async(domain: str):
    url = f"https://www.virustotal.com/api/v3/domains/{domain}"

    headers = {
        "accept": "application/json",
        "x-apikey": vt_api_key
    }

    response = requests.get(url, headers=headers)
    if response:
        session = create_session()
        add_data(session, domain, "virustotal", response.text, "domain_table")
