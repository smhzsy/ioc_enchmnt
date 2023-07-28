import os

import vt
from dotenv import load_dotenv

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")

def get_virustotal_hash_info(hash_value):
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


print(result.last_analysis_date)
print(result.first_submission_date)
print(result.last_analysis_results)
print(result.last_analysis_stats)
print(result.last_modification_date)
print(result.last_submission_date)
print(result.names)
print(result.reputation)
print(result.sandbox_verdicts)
print(result.sha1)
print(result.sha256)
print(result.md5)
print(result.size)
print(result.tags)
print(result.times_submitted)
print(result.total_votes)
print(result.type_description)
print(result.type_extension)
print(result.unique_sources)
print(result.vhash)
