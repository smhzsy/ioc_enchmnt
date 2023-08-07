import os

import requests
from dotenv import load_dotenv

import logger_config
from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

git_auth_token = os.getenv("GITHUB_AUTH_TOKEN")

logger_config.configure_logging()
logger = logger_config.get_logger()
error_logger = logger_config.get_error_logger()


async def search_in_bd_repo_async(search_ioc: str, table_name: str) -> None:
    """
    Searches ioc in the BRANDEFENSE GitHub ioc repository. Adds the data if the ioc is found.
    :param search_ioc: The ioc to search
    :param table_name: The table name in database to add datas.
    :return: Info with logs
    """
    repo_url = "https://api.github.com/repos/BRANDEFENSE/IoC"
    headers = {}
    if git_auth_token:
        headers["Authorization"] = f"Token {git_auth_token}"

    api_url = f"{repo_url}/contents"
    response = requests.get(api_url, headers=headers)
    session = create_session()
    if response.status_code == 200:
        files = response.json()
        found = False
        for file in files:
            if file["type"] == "file" and file["name"].endswith(".txt"):
                download_url = file["download_url"]
                content_response = requests.get(download_url, headers=headers)
                if content_response.status_code == 200:
                    file_content = content_response.text
                    if search_ioc in file_content:
                        add_data(
                            session,
                            search_ioc,
                            "brandefense_repo",
                            file["name"],
                            table_name,
                        )
                        logger.info("BRANDEFENSE info added.")
                        found = True
        if not found:
            add_data(
                session, search_ioc, "brandefense_repo", "IOC not found.", table_name
            )
            logger.info("IOC not found in Brandefense Repo")
    else:
        add_data(session, search_ioc, "brandefense_repo", "Error occurred.", table_name)
        error_logger.error(
            "Error while fetching data from GitHub API: " + str(response.status_code)
        )
