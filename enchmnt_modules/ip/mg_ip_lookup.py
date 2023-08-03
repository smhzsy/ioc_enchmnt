import requests

from database_files.add import add_data
from database_files.session import create_session


def mg_ip_lookup_async(ip_address):
    try:
        url = f"https://check.mertcan.dev/check.php?ip={ip_address}"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        session = create_session()
        add_data(session, ip_address, "mg_db", json_data, "ip_table")
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return None
    except ValueError as e:
        print("Error parsing JSON response:", e)
        return None


