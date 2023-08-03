import os
import aiohttp
import asyncio
from dotenv import load_dotenv

from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

av_api_key = os.getenv("ALIENVAULT_API_KEY")


async def search_indicator_in_alienvault_async(indicator_type, indicator_value, table_name):
    endpoint = f"https://otx.alienvault.com/api/v1/indicators/{indicator_type}/{indicator_value}/general"
    headers = {"X-OTX-API-KEY": av_api_key}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                response_data = await response.json()

                if response.status == 200:
                    session = create_session()
                    add_data(session, indicator_value, "alienvault", str(response_data), table_name)

                else:
                    print("Error: Unable to fetch data from AlienVault.")
                    return None

    except aiohttp.ClientError as e:
        print("Error: Client Error -", e)
        return None