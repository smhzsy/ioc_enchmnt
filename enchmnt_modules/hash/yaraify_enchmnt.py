import requests

from database_files.add import add_data
from database_files.session import create_session


async def yara_hash_lookup_async(hash_value:str):
    """
    API'ye verilen hash değerini sorgular ve sonuçları döndürür.

    Args:
        hash_value (str): Sorgulanacak hash değeri (SHA256, MD5, SHA1).

    Returns:
        dict: API'nin döndürdüğü JSON yanıtı.
    """
    headers = {'Content-Type': 'application/json'}
    data = {
        "query": "lookup_hash",
        "search_term": hash_value,
    }

    try:
        api_url = "https://yaraify-api.abuse.ch/api/v1/"
        response = requests.post(api_url, json=data, headers=headers)
        response_data = response.json()
        session = create_session()
        add_data(session, hash_value, "yaraify", str(response_data), "hash_table")
    except requests.RequestException as e:
        print(f"Hata oluştu: {e}")
        return None

