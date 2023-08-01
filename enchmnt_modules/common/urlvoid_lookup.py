import requests
import os

from dotenv import load_dotenv

load_dotenv()

apivoid_api_key = os.getenv("APIVOID_API_KEY")
def query_apivoid_api(url):
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


url_to_check = "https://www.sibergah.com/genel/internet-guvenligi/kotucul-siteleri-online-tespit-ve-tarama-araclari/"
api_response = query_apivoid_api(url_to_check)
print(api_response)
