import requests


def get_iq_info(keyword: str):
    url = f"https://labs.inquest.net/api/iocdb/search?keyword={keyword}&filter_by="
    response = requests.request("GET", url)
    print(response.text)

get_iq_info("88880772b0f8723020e0feb2bb179dc71e482072")