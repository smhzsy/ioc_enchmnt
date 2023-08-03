import os

import shodan
from dotenv import load_dotenv

from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

sh_api_key = os.getenv("SHODAN_API_KEY")


def shodan_lookup_async(ip):
    try:
        api = shodan.Shodan(sh_api_key)

        host = api.host(ip)

        session = create_session()
        add_data(session, ip, "shodan", host, "ip_table")
    except shodan.APIError as e:
        print("Hata: ", str(e))
