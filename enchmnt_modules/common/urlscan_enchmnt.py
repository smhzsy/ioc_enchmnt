import requests

def get_urlscan_info_async(type:str, keyword: str):
    url = f"https://urlscan.io/api/v1/search/?q={type}:{keyword}"
    response = requests.request("GET", url)
    print(response.text)
