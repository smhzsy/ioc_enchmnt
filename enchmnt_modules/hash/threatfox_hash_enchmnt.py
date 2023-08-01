import requests


def search_hash_threatfox(file_hash):
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
                return result['data']
            else:
                print('Error: API returned a query_status other than "ok"')
        else:
            print(f'Error: API request failed with status code {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

    return None


# Example usage:
file_hash_to_search = '2151c4b970eff0071948dbbc19066aa4'
search_result = search_hash_threatfox(file_hash_to_search)
print(search_result)
