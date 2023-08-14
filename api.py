import json

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from database_files.reader import get_data
from main import main

app = FastAPI()


@app.get("/search/")
async def search(ioc: str):
    """
    API method to send a request for searching IoC and returning the data found.
    :param ioc: Search string.
    :return: JSONResponse
    """
    await main(ioc)
    data = get_data(ioc)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
