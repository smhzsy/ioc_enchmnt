import requests

from database_files.add import add_data
from database_files.session import create_session


async def get_iq_info_async(keyword: str, table_name: str):
    url = f"https://labs.inquest.net/api/iocdb/search?keyword={keyword}&filter_by="
    response = requests.request("GET", url)
    session = create_session()
    add_data(session, keyword, "inquest", response.text, table_name)
