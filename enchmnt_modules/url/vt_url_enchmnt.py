import os

import requests
from dotenv import load_dotenv

from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")


def get_virustotal_url_info_async(url):
    scan_url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = {'apikey': vt_api_key, 'url': url}
    scan_response = requests.post(scan_url, params=params)
    scan_response_json = scan_response.json()

    if scan_response.status_code == 200:
        report_url = 'https://www.virustotal.com/vtapi/v2/url/report'
        params = {'apikey': vt_api_key, 'resource': scan_response_json['scan_id']}
        response = requests.get(report_url, params=params)
        response_json = response.json()

        if response.status_code == 200:
            session = create_session()
            add_data(session, url, "virustotal", str(response_json), "url_table")
        else:
            print('Error:', response_json['verbose_msg'])
    else:
        print('Error:', scan_response_json['verbose_msg'])
