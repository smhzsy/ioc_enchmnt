import requests

from database_files.add import add_data
from database_files.session import create_session


async def search_hash_threatfox_async(file_hash):
    url = 'https://threatfox-api.abuse.ch/api/v1/'
    headers = {'Content-Type': 'application/json'}
    data = {
        'query': 'search_hash',
        'hash': file_hash
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result['query_status'] == 'ok':
                session = create_session()
                add_data(session, file_hash, "threatfox", str(result['data']), "hash_table")
            else:
                print('Error: API returned a query_status other than "ok"')
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

    return None
