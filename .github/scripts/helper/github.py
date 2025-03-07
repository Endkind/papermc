from typing import List

import requests
from config import GithubConfig
from yarl import URL


class GithubHelper:
    _base_url = URL("https://api.github.com")

    @staticmethod
    def _get_base_repo_url(owner: str, name: str) -> URL:
        return GithubHelper._base_url / "repos" / owner / name

    @staticmethod
    def create_issue(
        title: str = "No Title Given",
        body: str = "No Body Given",
        assignees: List[str] = [],
        labels: List[str] = [],
        milestone: int = None,
        repo_owner: str = GithubConfig.REPO_OWNER,
        repo_name: str = GithubConfig.REPO_NAME,
        token: str = GithubConfig.TOKEN,
    ) -> bool:
        url = GithubHelper._get_base_repo_url(repo_owner, repo_name) / "issues"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}",
        }
        data = {
            "title": title,
            "body": body,
            "assignees": assignees,
            "labels": labels,
            "milestone": milestone,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            return True
        else:
            print(
                f'Error while creating the issue. Status code: "{response.status_code}". URL: "{url}"'
            )
            print(response.json())
            return False

    @staticmethod
    def get_repo_tags(
        repo_owner: str = GithubConfig.REPO_OWNER,
        repo_name: str = GithubConfig.REPO_NAME,
    ) -> List[str]:
        tags = []
        url = GithubHelper._get_base_repo_url(repo_owner, repo_name) / "tags"
        headers = {"Accept": "application/vnd.github.v3+json"}

        while True:
            response = requests.get(url, headers=headers)

            json = response.json()

            for entry in json:
                print(entry)  # DEBUG
                tags.append(entry["name"])

            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                break

        return tags

    @staticmethod
    def get_open_issues(
        repo_owner: str = GithubConfig.REPO_OWNER,
        repo_name: str = GithubConfig.REPO_NAME,
        token: str = GithubConfig.TOKEN,
    ):
        issues = []
        url = GithubHelper._get_base_repo_url(repo_owner, repo_name) / "issues"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {token}",
        }
        params = {"state": "open"}

        response = requests.get(url, headers=headers, params=params)

        json = response.json()

        for entry in json:
            issues.append(entry)

        return issues
