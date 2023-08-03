import os

import vt
from dotenv import load_dotenv

from celery_files.celery_config import app

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")



@app.task
def get_virustotal_hash_info_async(hash_value):
    client = vt.Client(vt_api_key)

    try:
        file_info = client.get_object(f"/files/{hash_value}")
        return file_info
    except vt.APIError as e:
        if e.code == "NotFoundError":
            return "Hash not found on VirusTotal."
        else:
            return "An error occurred while fetching data from VirusTotal."
    finally:
        client.close()
