import requests


def get_urlscan_info(type:str, keyword: str):
    url = f"https://urlscan.io/api/v1/search/?q={type}:{keyword}"
    response = requests.request("GET", url)
    print(response.text)

get_urlscan_info("ip","8.8.8.8")