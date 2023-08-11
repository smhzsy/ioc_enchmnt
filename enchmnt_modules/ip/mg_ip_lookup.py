import httpx
import logger_config
from database_files.add import add_data
from database_files.session import create_session
import pydash as _
logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def mg_ip_lookup_async(ip_address: str, result_list: list) -> None:
    """
    Searches IP IoC in Mertcan Gokgoz bad IP database. Writes all data found to database.
    :param result_list:
    :param ip_address:
    :return:
    """
    session = create_session()

    async with httpx.AsyncClient() as client:
        try:
            url = f"https://check.mertcan.dev/check.php?ip={ip_address}"
            response = await client.get(url)
            response.raise_for_status()
            json_data = response.json()

            if "false" in str(json_data):
                _.push(result_list, "'MertcanGokgoz': 'False'")
                result_str = "".join(result_list)
                add_data(session, ip_address, result_str, "result")
                logger.info("Mertcan Gokgoz ip info failed.")
            elif "invalid query" in str(json_data):
                _.push(result_list, "'MertcanGokgoz': 'TypeError'")
                result_str = "".join(result_list)
                add_data(session, ip_address, result_str, "result")
                logger.info("Mertcan Gokgoz ip info failed. (type error)")
            else:
                _.push(result_list, "'MertcanGokgoz': 'True'")
                result_str = "".join(result_list)
                add_data(session, ip_address, result_str, "result")
                logger.info("Mertcan Gokgoz ip info added.")
        except httpx.RequestError as e:
            _.push(result_list, "'MertcanGokgoz': 'Error'")
            result_str = "".join(result_list)
            add_data(session, ip_address, result_str, "result")
            error_logger.error("Error occurred while trying to fetch data from MG bad IP API: " + str(e))
