import os

import vt
from dotenv import load_dotenv

from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")


async def get_virustotal_hash_info_async(hash_value):
    client = vt.Client(vt_api_key)

    try:
        file_info = client.get_object(f"/files/{hash_value}")
        session = create_session()
        add_data(session, hash_value, "virustotal", file_info, "hash_table")
    except vt.APIError as e:
        if e.code == "NotFoundError":
            return "Hash not found on VirusTotal."
        else:
            return "An error occurred while fetching data from VirusTotal."
    finally:
        client.close()
