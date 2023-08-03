import os

import requests
from dotenv import load_dotenv

from database_files.add import add_data
from database_files.session import create_session

load_dotenv()

git_auth_token = os.getenv("GITHUB_AUTH_TOKEN")


async def search_in_bd_repo_async(search_ioc, table_name):
    repo_url = 'https://api.github.com/repos/BRANDEFENSE/IoC'
    headers = {}
    if git_auth_token:
        headers['Authorization'] = f'Token {git_auth_token}'

    api_url = f'{repo_url}/contents'
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file['type'] == 'file' and file['name'].endswith('.txt'):
                download_url = file['download_url']
                content_response = requests.get(download_url, headers=headers)
                if content_response.status_code == 200:
                    file_content = content_response.text
                    if search_ioc in file_content:
                        session = create_session()
                        add_data(session, search_ioc, "brandefense_repo", file['name'], table_name)
        return None
    else:
        print(f'Hata: GitHub API\'si dosya listesi alınamadı. Hata kodu: {response.status_code}')
        return None
