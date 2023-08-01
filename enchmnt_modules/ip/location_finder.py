import requests


def get_location(keyword: str):
    url = f"http://ip-api.com/json/{keyword}"
    response = requests.request("GET", url)
    print(response.text)


get_location("google.com")
