from typing import List
from yarl import URL

import requests

class PaperMCHelper:
    _base_url = URL('https://api.papermc.io/v2/projects')

    @staticmethod
    def _get_project_url(project: str) -> URL:
        return PaperMCHelper._base_url / project
    
    @staticmethod
    def get_project_versions(project: str) -> List[str]:
        url = PaperMCHelper._get_project_url(project)

        response = requests.get(url)

        return response.json()['versions']
