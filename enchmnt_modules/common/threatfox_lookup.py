import requests


def search_ioc_threatfox(ioc):
    url = 'https://threatfox-api.abuse.ch/api/v1/'
    headers = {'Content-Type': 'application/json'}
    data = {
        'query': 'search_ioc',
        'search_term': ioc
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

ioc_to_search = 'nyanmoney02.duckdns.org'
search_result = search_ioc_threatfox(ioc_to_search)
print(search_result)
