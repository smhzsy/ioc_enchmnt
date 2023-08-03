import requests

from database_files.add import add_data
from database_files.session import create_session


async def mg_domain_lookup_async(input_value):
    url = "https://raw.githubusercontent.com/mertcangokgoz/public-disavow-links/main/disavow-links.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        domains = response.text.splitlines()

        for domain in domains:
            if input_value.lower() in domain.lower():
                result = f"Input value '{input_value}' found in domain: {domain}"
                session = create_session()
                add_data(session, input_value, "mg_db", result, "domain_table")

        print(f"Input value '{input_value}' not found in any domain.")
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
