import asyncio
import time
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from database_files.data_getters.get_domain import get_domain_data
from database_files.data_getters.get_hash import get_hash_data
from database_files.data_getters.get_ip import get_ip_data
from database_files.data_getters.get_url import get_url_data
from enums import InputType
from input_identify import identify_input_type
from main import main
import uvicorn

app = FastAPI()


@app.get("/search/")
def search(ioc: str):
    """
    API method to send a request for searching IoC and returning the data found.
    :param ioc: Search string.
    :return: JSONResponse
    """
    data = None
    asyncio.run(main(ioc))
    time.sleep(10)
    ioc_type = identify_input_type(ioc)
    if ioc_type == InputType.URL:
        data = get_url_data(ioc)
    elif ioc_type == InputType.IP:
        data = get_ip_data(ioc)
    elif (
            ioc_type == InputType.MD5_HASH
            or ioc_type == InputType.SHA1_HASH
            or ioc_type == InputType.SHA256_HASH
    ):
        data = get_hash_data(ioc)
    elif ioc_type == InputType.DOMAIN:
        data = get_domain_data(ioc)

    row_dict = dict(data)
    return JSONResponse(content=row_dict)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
