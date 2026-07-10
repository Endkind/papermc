import requests
from config import PaperMCAPIConfig
from enums import PaperMCAPIProject
from yarl import URL


class PaperMCAPIUtils:
    @classmethod
    def get_all_versions(cls, project: PaperMCAPIProject) -> list[str]:
        base_url = URL(PaperMCAPIConfig.BASE_URL)

        url = base_url / project.value

        response = requests.get(url.__str__())

        all_versions = []

        for _, versions in response.json()["versions"].items():
            all_versions.extend(versions)

        return all_versions
