import requests
from config import PaperMCAPIConfig
from enums import PaperMCAPIProject
from result import Err, Ok, Result
from yarl import URL


class PaperMCAPIUtils:
    @classmethod
    def get_all_versions(cls, project: PaperMCAPIProject) -> Result[list[str], str]:
        base_url = URL(PaperMCAPIConfig.BASE_URL)

        url = base_url / project.value

        response = requests.get(url.__str__())

        if response.status_code != 200:
            return Err(
                f"Failed to fetch versions for project {project.value}. Status code: {response.status_code}"
            )

        all_versions = []

        for _, versions in response.json()["versions"].items():
            all_versions.extend(versions)

        return Ok(all_versions)
