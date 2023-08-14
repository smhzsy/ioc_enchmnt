import httpx
import pydash as _
import logger_config
from database_files.add import add_data
from database_files.session import create_session

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def get_location_async(keyword: str, info_list: list) -> None:
    """
    Getting the geometric location of ioc.
    :param info_list: The list of Data.
    :param keyword: Ioc to search
    :return: Info with logs
    """
    url = f"http://ip-api.com/json/{keyword}"

    async with httpx.AsyncClient() as client:
        session = create_session()
        try:
            response = await client.get(url)
            if response:
                response_data = response.json()

                country = response_data.get("country")
                city = response_data.get("city")
                lat = response_data.get("lat")
                lon = response_data.get("lon")

                _.push(info_list, f'"\'Country\'":"{country}",')
                _.push(info_list, f'"\'City\'":"{city}",')
                _.push(info_list, f'"\'Latitude\'":"{lat}",')
                _.push(info_list, f'"\'Longitude\'":"{lon}",')

                result_str = "".join(info_list)

                add_data(session, keyword, result_str, "info")
                logger.info("Location info added.")

            else:
                _.push(info_list, '"\'Location\'":"Not Found",')
                result_str = "".join(info_list)
                add_data(session, keyword, result_str, "info")
                logger.info("Location info failed.")

        except Exception as e:
            _.push(info_list,'"\'Location\'":"Error",')
            result_str = "".join(info_list)
            add_data(session, keyword, result_str, "info")
            error_logger.error("Error while trying to get Location Info: %s", str(e))
