import requests


def get_iq_info_async(keyword: str):
    url = f"https://labs.inquest.net/api/iocdb/search?keyword={keyword}&filter_by="
    response = requests.request("GET", url)
    print(response.text)
    print("success")
