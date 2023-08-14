import os

import httpx
import pydash as _
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

git_auth_token = os.getenv("GITHUB_AUTH_TOKEN")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_in_bd_repo_async(search_ioc: str, result_list: list) -> None:
    """
    Searches ioc in the BRANDEFENSE GitHub ioc repository. Adds the data if the ioc is found.
    :param result_list: The result list.
    :param search_ioc: The ioc to search.
    :return: Info with logs.
    """
    repo_url = "https://api.github.com/repos/BRANDEFENSE/IoC"
    headers = {}
    if git_auth_token:
        headers["Authorization"] = f"Token {git_auth_token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(repo_url + "/contents", headers=headers)
        if response.status_code == 200:
            files = response.json()
            found = False
            for file in files:
                if file["type"] == "file" and file["name"].endswith(".txt"):
                    download_url = file["download_url"]
                    content_response = await client.get(download_url, headers=headers)
                    if content_response.status_code == 200:
                        file_content = content_response.text
                        if search_ioc in file_content:
                            _.push(result_list, '"\'Brandefense\'":"True",')
                            result_str = "".join(result_list)
                            session = create_session()
                            add_data(session, search_ioc, result_str, "result")
                            logger.info("BRANDEFENSE info added.")
                            found = True
                            break
            if not found:
                _.push(result_list, '"\'Brandefense\'":"False",')
                result_str = "".join(result_list)
                session = create_session()
                add_data(session, search_ioc, result_str, "result")
                logger.info("IOC not found in Brandefense Repo")
        else:
            _.push(result_list, '"\'Brandefense\'":"Error",')
            result_str = "".join(result_list)
            session = create_session()
            add_data(session, search_ioc, result_str, "result")
            error_logger.error(
                "Error while fetching data from GitHub API: " + str(response.status_code)
            )
