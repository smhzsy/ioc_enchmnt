import datetime
import os

import requests
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
load_dotenv()

vt_api_key = os.getenv("VT_API_KEY")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_virustotal_url_info_async(url: str, result_list: list) -> None:
    """
    Scans the url type ioc in virustotal. Adds the results to database.
    :param result_list:
    :param url: the ioc
    :return: info with logs
    """
    session = create_session()
    try:
        scan_url = "https://www.virustotal.com/vtapi/v2/url/scan"
        params = {"apikey": vt_api_key, "url": url}
        scan_response = requests.post(scan_url, params=params)
        scan_response_json = scan_response.json()

        if scan_response.status_code == 200:
            report_url = "https://www.virustotal.com/vtapi/v2/url/report"
            params = {"apikey": vt_api_key, "resource": scan_response_json["scan_id"]}
            response = requests.get(report_url, params=params)

            if response.status_code == 200:
                _.push(result_list, "'VirusTotal': 'True'")
                result_str = "".join(result_list)
                add_data(session, url, result_str, "result")
                logger.info("VirusTotal info added.")
            else:
                _.push(result_list, "'VirusTotal': 'False'")
                result_str = "".join(result_list)
                add_data(session, url, result_str, "result")
                logger.info("VirusTotal info failed.")
        else:
            _.push(result_list, "'VirusTotal': 'Error'")
            result_str = "".join(result_list)
            add_data(session, url, result_str, "result")
            error_logger.error(
                "Virustotal got an error while scanning."
                + str(scan_response_json["verbose_msg"])
            )
    except Exception as e:
        _.push(result_list, "'VirusTotal': 'Error'")
        result_str = "".join(result_list)
        add_data(session, url, result_str, "result")
        error_logger.error("Virustotal got an error while scanning." + str(e))
